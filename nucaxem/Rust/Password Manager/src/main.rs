use aes::Aes256;
use block_modes::{BlockMode, Cbc};
use block_modes::block_padding::Pkcs7;
use pbkdf2::pbkdf2_hmac;
use rand::Rng;
use sha2::Sha256;
use serde::{Serialize, Deserialize};
use std::fs::{self, File};
use std::io::{BufReader, Read};
use std::path::Path;
use base64::{encode, decode};
use clipboard::{ClipboardContext, ClipboardProvider};
use rpassword::read_password;
use eframe::{egui, epi};
use egui::{RichText, Color32};
use std::collections::HashMap;

type Aes256Cbc = Cbc<Aes256, Pkcs7>;

const DB_FILE: &str = "passman.json";

#[derive(Serialize, Deserialize, Clone)]
struct PasswordEntry {
    service: String,
    username: String,
    password: String,
}

#[derive(Serialize, Deserialize)]
struct Database {
    salt: String,
    encrypted: String,
}

fn generate_salt() -> Vec<u8> {
    let mut salt = [0u8; 32];
    rand::thread_rng().fill(&mut salt);
    salt.to_vec()
}

fn derive_key(master: &str, salt: &[u8]) -> [u8; 32] {
    let mut key = [0u8; 32];
    pbkdf2_hmac::<Sha256>(master.as_bytes(), salt, 200_000, &mut key);
    key
}

fn encrypt_json(json: &str, key: &[u8]) -> Vec<u8> {
    let mut iv = [0u8; 16];
    rand::thread_rng().fill(&mut iv);
    let cipher = Aes256Cbc::new_from_slices(key, &iv).unwrap();
    let mut encrypted = cipher.encrypt_vec(json.as_bytes());
    let mut combined = iv.to_vec();
    combined.append(&mut encrypted);
    combined
}

fn decrypt_json(data: &[u8], key: &[u8]) -> Option<String> {
    if data.len() < 16 { return None; }
    let iv = &data[..16];
    let ciphertext = &data[16..];
    let cipher = Aes256Cbc::new_from_slices(key, iv).ok()?;
    let decrypted = cipher.decrypt_vec(ciphertext).ok()?;
    String::from_utf8(decrypted).ok()
}

fn load_or_create_db(master: &str) -> (Vec<PasswordEntry>, [u8;32], Vec<u8>) {
    if !Path::new(DB_FILE).exists() {
        let salt = generate_salt();
        let key = derive_key(master, &salt);
        let empty: Vec<PasswordEntry> = vec![];
        let encrypted = encrypt_json(&serde_json::to_string(&empty).unwrap(), &key);
        let db = Database {
            salt: encode(&salt),
            encrypted: encode(&encrypted),
        };
        fs::write(DB_FILE, serde_json::to_string_pretty(&db).unwrap()).unwrap();
        return (empty, key, salt);
    }

    let file = File::open(DB_FILE).unwrap();
    let reader = BufReader::new(file);
    let db: Database = serde_json::from_reader(reader).unwrap();
    let salt = decode(db.salt).unwrap();
    let key = derive_key(master, &salt);
    let encrypted = decode(db.encrypted).unwrap();
    let entries = decrypt_json(&encrypted, &key)
        .and_then(|s| serde_json::from_str(&s).ok())
        .unwrap_or_else(|| vec![]);
    (entries, key, salt)
}

fn save_db(entries: &[PasswordEntry], key: &[u8], salt: &[u8]) {
    let json = serde_json::to_string_pretty(entries).unwrap();
    let encrypted = encrypt_json(&json, key);
    let db = Database {
        salt: encode(salt),
        encrypted: encode(&encrypted),
    };
    fs::write(DB_FILE, serde_json::to_string_pretty(&db).unwrap()).unwrap();
}

// Simple password strength checker
fn password_strength(pw: &str) -> (usize, &'static str) {
    let mut score = 0;
    if pw.len() >= 8 { score += 1; }
    if pw.chars().any(|c| c.is_uppercase()) { score += 1; }
    if pw.chars().any(|c| c.is_lowercase()) { score += 1; }
    if pw.chars().any(|c| c.is_numeric()) { score += 1; }
    if pw.chars().any(|c| !c.is_alphanumeric()) { score += 1; }
    let text = match score {
        0..=1 => "Very Weak",
        2 => "Weak",
        3 => "Medium",
        4 => "Strong",
        _ => "Very Strong",
    };
    (score, text)
}

// Password generator
fn generate_password(len: usize) -> String {
    const CHARSET: &[u8] = b"ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*()-_=+[]{}|;:,.<>?";
    let mut rng = rand::thread_rng();
    (0..len).map(|_| {
        let idx = rng.gen_range(0..CHARSET.len());
        CHARSET[idx] as char
    }).collect()
}

struct PassmanApp {
    entries: Vec<PasswordEntry>,
    master_key: [u8;32],
    salt: Vec<u8>,
    search: String,
    new_service: String,
    new_username: String,
    new_password: String,
    show_passwords: bool,
    copy_message: String,
}

impl PassmanApp {
    fn filtered_entries(&self) -> Vec<&PasswordEntry> {
        if self.search.is_empty() {
            self.entries.iter().collect()
        } else {
            self.entries.iter()
                .filter(|e| e.service.to_lowercase().contains(&self.search.to_lowercase()))
                .collect()
        }
    }
}

impl epi::App for PassmanApp {
    fn name(&self) -> &str { "Modern PassMan" }

    fn update(&mut self, ctx: &egui::Context, _frame: &mut epi::Frame) {
        egui::CentralPanel::default().show(ctx, |ui| {
            ui.horizontal(|ui| {
                ui.label(RichText::new("Search:").strong());
                ui.text_edit_singleline(&mut self.search);
                if ui.button("Clear").clicked() {
                    self.search.clear();
                }
            });

            ui.separator();

            for entry in self.filtered_entries() {
                ui.group(|ui| {
                    ui.horizontal(|ui| {
                        ui.label(RichText::new(&entry.service).strong());
                        if ui.button("Copy User").clicked() {
                            let mut ctx: ClipboardContext = ClipboardProvider::new().unwrap();
                            ctx.set_contents(entry.username.clone()).unwrap();
                            self.copy_message = format!("Copied username of {}", entry.service);
                        }
                        if ui.button("Copy Pass").clicked() {
                            let mut ctx: ClipboardContext = ClipboardProvider::new().unwrap();
                            ctx.set_contents(entry.password.clone()).unwrap();
                            self.copy_message = format!("Copied password of {}", entry.service);
                        }
                        if self.show_passwords {
                            ui.label(format!("Password: {}", entry.password));
                        }
                    });
                });
            }

            if !self.copy_message.is_empty() {
                ui.colored_label(Color32::LIGHT_GREEN, &self.copy_message);
            }

            ui.separator();
            ui.horizontal(|ui| {
                ui.checkbox(&mut self.show_passwords, "Show Passwords");
            });

            ui.group(|ui| {
                ui.label(RichText::new("Add New Entry").strong());
                ui.horizontal(|ui| {
                    ui.label("Service:");
                    ui.text_edit_singleline(&mut self.new_service);
                });
                ui.horizontal(|ui| {
                    ui.label("Username:");
                    ui.text_edit_singleline(&mut self.new_username);
                });
                ui.horizontal(|ui| {
                    ui.label("Password:");
                    ui.text_edit_singleline(&mut self.new_password);
                    if ui.button("Gen").clicked() {
                        self.new_password = generate_password(16);
                    }
                });

                if !self.new_password.is_empty() {
                    let (score, text) = password_strength(&self.new_password);
                    let color = match score {
                        0..=1 => Color32::RED,
                        2 => Color32::YELLOW,
                        3 => Color32::LIGHT_YELLOW,
                        4 => Color32::LIGHT_GREEN,
                        _ => Color32::GREEN,
                    };
                    ui.colored_label(color, format!("Strength: {}", text));
                }

                if ui.button("Add Entry").clicked() {
                    if !self.new_service.is_empty() && !self.new_username.is_empty() && !self.new_password.is_empty() {
                        self.entries.push(PasswordEntry {
                            service: self.new_service.clone(),
                            username: self.new_username.clone(),
                            password: self.new_password.clone(),
                        });
                        save_db(&self.entries, &self.master_key, &self.salt);
                        self.new_service.clear();
                        self.new_username.clear();
                        self.new_password.clear();
                    }
                }
            });
        });
    }
}

fn main() {
    println!("Enter master password:");
    let master = read_password().unwrap();
    let (entries, key, salt) = load_or_create_db(&master);

    let app = PassmanApp {
        entries,
        master_key: key,
        salt,
        search: "".to_string(),
        new_service: "".to_string(),
        new_username: "".to_string(),
        new_password: "".to_string(),
        show_passwords: false,
        copy_message: "".to_string(),
    };

    let native_options = eframe::NativeOptions {
        initial_window_size: Some(egui::vec2(800.0, 600.0)),
        ..Default::default()
    };
    eframe::run_native(Box::new(app), native_options);
  }
