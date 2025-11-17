use image::{DynamicImage, GenericImageView, ImageBuffer, Rgba};
use std::io::{self, Write};

fn main() {
    println!("--- Rust Image Editor ---");
    println!("Load an image to begin.");

    let mut img = loop {
        match prompt_load_image() {
            Ok(i) => break i,
            Err(e) => println!("Error: {}", e),
        }
    };

    loop {
        println!("\nMenu:");
        println!("1) Grayscale");
        println!("2) Invert colors");
        println!("3) Brightness");
        println!("4) Blur");
        println!("5) Sharpen");
        println!("6) Crop");
        println!("7) Resize");
        println!("8) Save");
        println!("9) Exit");

        let input = prompt("Choose option: ");
        match input.trim() {
            "1" => { img = apply_grayscale(&img); println!("Applied grayscale."); }
            "2" => { img = apply_invert(&img); println!("Inverted."); }
            "3" => {
                let val = prompt("Brightness change (-255..255): ");
                if let Ok(v) = val.trim().parse::<i32>() {
                    img = apply_brightness(&img, v);
                    println!("Brightness applied.");
                }
            }
            "4" => {
                let val = prompt("Blur radius: ");
                if let Ok(v) = val.trim().parse::<f32>() {
                    img = img.blur(v);
                    println!("Blur applied.");
                }
            }
            "5" => {
                img = apply_sharpen(&img);
                println!("Sharpen applied.");
            }
            "6" => {
                let x = prompt("x: ").trim().parse().unwrap_or(0);
                let y = prompt("y: ").trim().parse().unwrap_or(0);
                let w = prompt("width: ").trim().parse().unwrap_or(100);
                let h = prompt("height: ").trim().parse().unwrap_or(100);
                img = crop_image(&img, x, y, w, h);
                println!("Cropped.");
            }
            "7" => {
                let w = prompt("new width: ").trim().parse().unwrap_or(100);
                let h = prompt("new height: ").trim().parse().unwrap_or(100);
                img = img.resize_exact(w, h, image::imageops::FilterType::CatmullRom);
                println!("Resized.");
            }
            "8" => {
                match prompt_save_image(&img) {
                    Ok(_) => println!("Saved."),
                    Err(e) => println!("Error saving: {}", e),
                }
            }
            "9" => break,
            _ => println!("Invalid option."),
        }
    }

    println!("Goodbye!");
}

fn prompt(text: &str) -> String {
    print!("{}", text);
    io::stdout().flush().unwrap();
    let mut s = String::new();
    io::stdin().read_line(&mut s).unwrap();
    s
}

fn prompt_load_image() -> Result<DynamicImage, String> {
    let path = prompt("Enter image path: ").trim().to_string();
    image::open(&path).map_err(|e| e.to_string())
}

fn prompt_save_image(img: &DynamicImage) -> Result<(), String> {
    let path = prompt("Save as (path): ").trim().to_string();
    img.save(path).map_err(|e| e.to_string())
}

fn apply_grayscale(img: &DynamicImage) -> DynamicImage {
    let (w, h) = img.dimensions();
    let mut out = ImageBuffer::<Rgba<u8>, Vec<u8>>::new(w, h);

    for (x, y, pixel) in img.pixels() {
        let [r, g, b, a] = pixel.0;
        let gray = (0.3 * r as f32 + 0.59 * g as f32 + 0.11 * b as f32) as u8;
        out.put_pixel(x, y, Rgba([gray, gray, gray, a]));
    }
    DynamicImage::ImageRgba8(out)
}

fn apply_invert(img: &DynamicImage) -> DynamicImage {
    let (w, h) = img.dimensions();
    let mut out = ImageBuffer::<Rgba<u8>, Vec<u8>>::new(w, h);

    for (x, y, pixel) in img.pixels() {
        let [r, g, b, a] = pixel.0;
        out.put_pixel(x, y, Rgba([255 - r, 255 - g, 255 - b, a]));
    }
    DynamicImage::ImageRgba8(out)
}

fn apply_brightness(img: &DynamicImage, amount: i32) -> DynamicImage {
    let (w, h) = img.dimensions();
    let mut out = ImageBuffer::<Rgba<u8>, Vec<u8>>::new(w, h);

    for (x, y, pixel) in img.pixels() {
        let [r, g, b, a] = pixel.0;
        out.put_pixel(
            x,
            y,
            Rgba([
                clamp(r as i32 + amount),
                clamp(g as i32 + amount),
                clamp(b as i32 + amount),
                a,
            ]),
        );
    }
    DynamicImage::ImageRgba8(out)
}

fn clamp(v: i32) -> u8 {
    v.max(0).min(255) as u8
}

fn crop_image(img: &DynamicImage, x: u32, y: u32, w: u32, h: u32) -> DynamicImage {
    let cropped = image::imageops::crop_imm(img, x, y, w, h);
    DynamicImage::ImageRgba8(cropped.to_image())
}

fn apply_sharpen(img: &DynamicImage) -> DynamicImage {
    // Simple sharpening kernel
    let kernel: [[f32; 3]; 3] = [
        [0.0, -1.0, 0.0],
        [-1.0, 5.0, -1.0],
        [0.0, -1.0, 0.0],
    ];

    convolve(img, &kernel)
}

fn convolve(img: &DynamicImage, kernel: &[[f32; 3]; 3]) -> DynamicImage {
    let (w, h) = img.dimensions();
    let mut out = ImageBuffer::<Rgba<u8>, Vec<u8>>::new(w, h);

    for y in 0..h {
        for x in 0..w {
            let mut r = 0.0;
            let mut g = 0.0;
            let mut b = 0.0;

            for ky in 0..3 {
                for kx in 0..3 {
                    let px = x as i32 + kx as i32 - 1;
                    let py = y as i32 + ky as i32 - 1;

                    if px < 0 || py < 0 || px >= w as i32 || py >= h as i32 {
                        continue;
                    }

                    let p = img.get_pixel(px as u32, py as u32).0;
                    r += kernel[ky][kx] * p[0] as f32;
                    g += kernel[ky][kx] * p[1] as f32;
                    b += kernel[ky][kx] * p[2] as f32;
                }
            }

            out.put_pixel(
                x,
                y,
                Rgba([
                    clamp(r as i32),
                    clamp(g as i32),
                    clamp(b as i32),
                    255,
                ]),
            );
        }
    }

    DynamicImage::ImageRgba8(out)
                  }
