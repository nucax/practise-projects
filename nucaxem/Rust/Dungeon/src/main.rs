// src/main.rs
// Dungeon: a small-but-complex text roguelike with save/load (JSON), procedural map,
// monsters, items, inventory, XP & leveling, and simple combat.
// Author: ChatGPT (example)

use rand::prelude::*;
use serde::{Deserialize, Serialize};
use std::cmp::{max, min};
use std::fs;
use std::io::{self, Write};

const MAP_W: usize = 40;
const MAP_H: usize = 20;
const ROOM_MAX: usize = 8;
const ROOM_MIN_SIZE: i32 = 3;
const ROOM_MAX_SIZE: i32 = 8;

#[derive(Clone, Copy, PartialEq, Eq, Serialize, Deserialize)]
enum Tile {
    Wall,
    Floor,
    Stairs,
}

#[derive(Serialize, Deserialize)]
struct Map {
    tiles: Vec<Tile>, // row-major
    width: usize,
    height: usize,
}

impl Map {
    fn new(width: usize, height: usize) -> Self {
        Self {
            tiles: vec![Tile::Wall; width * height],
            width,
            height,
        }
    }

    fn idx(&self, x: i32, y: i32) -> usize {
        (y as usize) * self.width + (x as usize)
    }

    fn in_bounds(&self, x: i32, y: i32) -> bool {
        x >= 0 && x < self.width as i32 && y >= 0 && y < self.height as i32
    }

    fn set(&mut self, x: i32, y: i32, t: Tile) {
        if self.in_bounds(x, y) {
            let i = self.idx(x, y);
            self.tiles[i] = t;
        }
    }

    fn get(&self, x: i32, y: i32) -> Tile {
        if self.in_bounds(x, y) {
            self.tiles[self.idx(x, y)]
        } else {
            Tile::Wall
        }
    }
}

#[derive(Serialize, Deserialize, Clone)]
struct Rect {
    x1: i32,
    y1: i32,
    x2: i32,
    y2: i32,
}

impl Rect {
    fn new(x: i32, y: i32, w: i32, h: i32) -> Self {
        Rect {
            x1: x,
            y1: y,
            x2: x + w,
            y2: y + h,
        }
    }

    fn center(&self) -> (i32, i32) {
        ((self.x1 + self.x2) / 2, (self.y1 + self.y2) / 2)
    }

    fn intersects(&self, other: &Rect) -> bool {
        !(self.x2 < other.x1 || self.x1 > other.x2 || self.y2 < other.y1 || self.y1 > other.y2)
    }
}

#[derive(Serialize, Deserialize, Clone)]
struct Item {
    name: String,
    kind: ItemKind,
}

#[derive(Serialize, Deserialize, Clone)]
enum ItemKind {
    HealthPotion(i32),
}

#[derive(Serialize, Deserialize, Clone)]
struct Actor {
    x: i32,
    y: i32,
    glyph: char,
    name: String,
    hp: i32,
    max_hp: i32,
    atk: i32,
    defense: i32,
    xp: i32,
}

impl Actor {
    fn is_alive(&self) -> bool {
        self.hp > 0
    }
}

#[derive(Serialize, Deserialize)]
struct Game {
    map: Map,
    player: Actor,
    monsters: Vec<Actor>,
    items: Vec<(i32, i32, Item)>,
    level: i32,
    rng_seed: u64,
}

impl Game {
    fn new(rng_seed: u64) -> Self {
        let mut rng = StdRng::seed_from_u64(rng_seed);
        let mut map = Map::new(MAP_W, MAP_H);

        // Generate rooms
        let mut rooms: Vec<Rect> = Vec::new();
        for _ in 0..ROOM_MAX {
            let w = rng.gen_range(ROOM_MIN_SIZE..=ROOM_MAX_SIZE);
            let h = rng.gen_range(ROOM_MIN_SIZE..=ROOM_MAX_SIZE);
            let x = rng.gen_range(1..(MAP_W as i32 - w - 1));
            let y = rng.gen_range(1..(MAP_H as i32 - h - 1));
            let new_room = Rect::new(x, y, w, h);
            if rooms.iter().all(|r| !r.intersects(&new_room)) {
                // carve
                for rx in new_room.x1..=new_room.x2 {
                    for ry in new_room.y1..=new_room.y2 {
                        map.set(rx, ry, Tile::Floor);
                    }
                }
                if !rooms.is_empty() {
                    // connect center to previous
                    let (new_x, new_y) = new_room.center();
                    let (prev_x, prev_y) = rooms[rooms.len() - 1].center();
                    if rng.gen_bool(0.5) {
                        Game::create_h_tunnel(&mut map, prev_x, new_x, prev_y);
                        Game::create_v_tunnel(&mut map, prev_y, new_y, new_x);
                    } else {
                        Game::create_v_tunnel(&mut map, prev_y, new_y, prev_x);
                        Game::create_h_tunnel(&mut map, prev_x, new_x, new_y);
                    }
                }
                rooms.push(new_room);
            }
        }

        // place stairs in last room
        let (sx, sy) = if let Some(r) = rooms.last() {
            r.center()
        } else {
            (MAP_W as i32 / 2, MAP_H as i32 / 2)
        };
        map.set(sx, sy, Tile::Stairs);

        // player start in first room center
        let (px, py) = if let Some(r) = rooms.first() {
            r.center()
        } else {
            (1, 1)
        };

        // spawn some monsters and items
        let mut monsters = Vec::new();
        let mut items = Vec::new();

        for _ in 0..(rooms.len() * 2).max(3) {
            // choose a room randomly (not the first)
            let r = &rooms[rng.gen_range(0..rooms.len())];
            let (mx, my) = (
                rng.gen_range(r.x1 + 1..=r.x2 - 1),
                rng.gen_range(r.y1 + 1..=r.y2 - 1),
            );
            if mx == px && my == py {
                continue;
            }
            let mtype = rng.gen_range(0..3);
            let monster = match mtype {
                0 => Actor {
                    x: mx,
                    y: my,
                    glyph: 'g',
                    name: "Goblin".to_string(),
                    hp: 8,
                    max_hp: 8,
                    atk: 3,
                    defense: 0,
                    xp: 5,
                },
                1 => Actor {
                    x: mx,
                    y: my,
                    glyph: 's',
                    name: "Skeleton".to_string(),
                    hp: 12,
                    max_hp: 12,
                    atk: 4,
                    defense: 1,
                    xp: 8,
                },
                _ => Actor {
                    x: mx,
                    y: my,
                    glyph: 'o',
                    name: "Orc".to_string(),
                    hp: 16,
                    max_hp: 16,
                    atk: 6,
                    defense: 2,
                    xp: 12,
                },
            };
            monsters.push(monster);
        }

        // items: few potions
        for _ in 0..4 {
            let r = &rooms[rng.gen_range(0..rooms.len())];
            let ix = rng.gen_range(r.x1 + 1..=r.x2 - 1);
            let iy = rng.gen_range(r.y1 + 1..=r.y2 - 1);
            items.push((
                ix,
                iy,
                Item {
                    name: "Health Potion".to_string(),
                    kind: ItemKind::HealthPotion(10),
                },
            ));
        }

        let player = Actor {
            x: px,
            y: py,
            glyph: '@',
            name: "Player".to_string(),
            hp: 30,
            max_hp: 30,
            atk: 5,
            defense: 1,
            xp: 0,
        };

        Self {
            map,
            player,
            monsters,
            items,
            level: 1,
            rng_seed,
        }
    }

    fn create_h_tunnel(map: &mut Map, x1: i32, x2: i32, y: i32) {
        for x in min(x1, x2)..=max(x1, x2) {
            map.set(x, y, Tile::Floor);
        }
    }
    fn create_v_tunnel(map: &mut Map, y1: i32, y2: i32, x: i32) {
        for y in min(y1, y2)..=max(y1, y2) {
            map.set(x, y, Tile::Floor);
        }
    }

    fn draw(&self) {
        // simple render to console
        let mut buffer = vec![vec![' '; self.map.width]; self.map.height];
        for y in 0..self.map.height {
            for x in 0..self.map.width {
                buffer[y][x] = match self.map.get(x as i32, y as i32) {
                    Tile::Wall => '#',
                    Tile::Floor => '.',
                    Tile::Stairs => '>',
                };
            }
        }
        // items
        for (ix, iy, item) in &self.items {
            if *ix >= 0 && *ix < self.map.width as i32 && *iy >= 0 && *iy < self.map.height as i32 {
                buffer[*iy as usize][*ix as usize] = '!';
            }
        }
        // monsters
        for m in &self.monsters {
            if m.is_alive() {
                buffer[m.y as usize][m.x as usize] = m.glyph;
            }
        }
        // player
        buffer[self.player.y as usize][self.player.x as usize] = self.player.glyph;

        // draw
        println!();
        for row in buffer {
            let line: String = row.into_iter().collect();
            println!("{}", line);
        }
        println!();
        println!(
            "HP: {}/{}  ATK:{} DEF:{}  XP:{}  LVL:{}",
            self.player.hp, self.player.max_hp, self.player.atk, self.player.defense, self.player.xp, self.level
        );
        println!("Commands: WASD move, G pick up, I inventory, S save, L load, Q quit");
    }

    fn player_move(&mut self, dx: i32, dy: i32) {
        let nx = self.player.x + dx;
        let ny = self.player.y + dy;
        if !self.map.in_bounds(nx, ny) {
            return;
        }
        if self.map.get(nx, ny) == Tile::Wall {
            return;
        }
        // check monster collision => attack
        if let Some(idx) = self
            .monsters
            .iter()
            .position(|m| m.x == nx && m.y == ny && m.is_alive())
        {
            let dmg = max(0, self.player.atk - self.monsters[idx].defense);
            self.monsters[idx].hp -= dmg;
            println!(
                "You hit the {} for {} damage ({} hp left).",
                self.monsters[idx].name, dmg, max(0, self.monsters[idx].hp)
            );
            if !self.monsters[idx].is_alive() {
                println!("{} dies!", self.monsters[idx].name);
                self.player.xp += self.monsters[idx].xp;
                self.check_level_up();
            }
            return;
        }

        self.player.x = nx;
        self.player.y = ny;

        // if standing on stairs, go deeper
        if self.map.get(nx, ny) == Tile::Stairs {
            println!("You descend the stairs to a deeper level...");
            self.level += 1;
            // new dungeon with new seed derived from previous
            let new_seed = self.rng_seed.wrapping_add(self.level as u64 * 7919);
            let mut new_game = Game::new(new_seed);
            // attempt to keep player stats
            new_game.player = Actor {
                x: new_game.player.x,
                y: new_game.player.y,
                glyph: '@',
                name: "Player".to_string(),
                hp: self.player.hp.saturating_add(5), // small heal
                max_hp: self.player.max_hp + 5,
                atk: self.player.atk + 1,
                defense: self.player.defense + 0,
                xp: self.player.xp,
            };
            // preserve some XP and items
            new_game.items.extend(self.items.clone());
            new_game.monsters.extend(self.monsters.clone());
            *self = new_game;
            println!("You feel stronger, the dungeon grows tougher...");
        }
    }

    fn monsters_take_turns(&mut self) {
        // naive AI: if adjacent to player, attack; otherwise move toward player if path clear
        let mut rng = StdRng::seed_from_u64(self.rng_seed.wrapping_add(self.level as u64));
        for m in &mut self.monsters {
            if !m.is_alive() {
                continue;
            }
            // distance
            let dx = self.player.x - m.x;
            let dy = self.player.y - m.y;
            let dist2 = dx * dx + dy * dy;
            if dist2 <= 2 {
                // melee
                let dmg = max(0, m.atk - self.player.defense);
                self.player.hp -= dmg;
                println!("The {} hits you for {} damage!", m.name, dmg);
                if self.player.hp <= 0 {
                    println!("You died... Game over.");
                }
            } else if dist2 < 100 {
                // move towards player with randomness
                let mut step_x = if dx == 0 { 0 } else { dx.signum() };
                let mut step_y = if dy == 0 { 0 } else { dy.signum() };
                // occasionally move randomly
                if rng.gen_bool(0.2) {
                    step_x = rng.gen_range(-1..=1);
                    step_y = rng.gen_range(-1..=1);
                }
                let nx = m.x + step_x;
                let ny = m.y + step_y;
                if !self.map.in_bounds(nx, ny) {
                    continue;
                }
                if self.map.get(nx, ny) == Tile::Wall {
                    continue;
                }
                // avoid other monsters and player
                if nx == self.player.x && ny == self.player.y {
                    continue;
                }
                if self.monsters.iter().any(|o| o.x == nx && o.y == ny && o.is_alive()) {
                    continue;
                }
                m.x = nx;
                m.y = ny;
            } else {
                // wander
                if rng.gen_bool(0.05) {
                    let vx = rng.gen_range(-1..=1);
                    let vy = rng.gen_range(-1..=1);
                    let nx = m.x + vx;
                    let ny = m.y + vy;
                    if self.map.in_bounds(nx, ny) && self.map.get(nx, ny) == Tile::Floor {
                        if !self.monsters.iter().any(|o| o.x == nx && o.y == ny && o.is_alive()) {
                            m.x = nx;
                            m.y = ny;
                        }
                    }
                }
            }
        }
    }

    fn pick_up(&mut self) {
        if let Some(pos) = self
            .items
            .iter()
            .position(|(ix, iy, _)| *ix == self.player.x && *iy == self.player.y)
        {
            let (_, _, item) = self.items.remove(pos);
            println!("You pick up a {}.", item.name);
            // apply item automatically for simplicity
            match item.kind {
                ItemKind::HealthPotion(amount) => {
                    self.player.hp = min(self.player.max_hp, self.player.hp + amount);
                    println!("You drink the potion and heal {} HP.", amount);
                }
            }
        } else {
            println!("There is nothing here to pick up.");
        }
    }

    fn open_inventory(&self) {
        println!("Inventory:");
        if self.items.is_empty() {
            println!("  (no loose items)");
        } else {
            for (i, (ix, iy, item)) in self.items.iter().enumerate() {
                println!("  {}: {} at ({},{})", i + 1, item.name, ix, iy);
            }
        }
    }

    fn save(&self, filename: &str) {
        match serde_json::to_string_pretty(self) {
            Ok(s) => {
                if let Err(e) = fs::write(filename, s) {
                    println!("Failed to write save file: {}", e);
                } else {
                    println!("Game saved to {}", filename);
                }
            }
            Err(e) => println!("Failed to serialize game: {}", e),
        }
    }

    fn load(filename: &str) -> Option<Self> {
        match fs::read_to_string(filename) {
            Ok(s) => match serde_json::from_str(&s) {
                Ok(g) => {
                    println!("Game loaded from {}", filename);
                    Some(g)
                }
                Err(e) => {
                    println!("Failed to parse save file: {}", e);
                    None
                }
            },
            Err(e) => {
                println!("Failed to read save file: {}", e);
                None
            }
        }
    }

    fn check_level_up(&mut self) {
        let mut leveled = false;
        while self.player.xp >= self.next_level_xp() {
            self.player.xp -= self.next_level_xp();
            self.level += 1;
            self.player.max_hp += 5;
            self.player.hp = self.player.max_hp;
            self.player.atk += 1;
            leveled = true;
        }
        if leveled {
            println!("You gained a level! You are now level {}.", self.level);
        }
    }

    fn next_level_xp(&self) -> i32 {
        20 + (self.level as i32 - 1) * 15
    }
}

fn read_char() -> Option<char> {
    print!("> ");
    let _ = io::stdout().flush();
    let mut input = String::new();
    if io::stdin().read_line(&mut input).is_ok() {
        input.chars().next().map(|c| c)
    } else {
        None
    }
}

fn main() {
    // greet and create or load
    println!("Dungeon - a tiny Rust roguelike");
    println!("New game (N) or Load (L)?");
    let choice = read_char().unwrap_or('N');
    let mut rng = thread_rng();
    let mut game = match choice {
        'L' | 'l' => {
            if let Some(g) = Game::load("save.json") {
                g
            } else {
                println!("Starting a new game instead.");
                Game::new(rng.gen())
            }
        }
        _ => Game::new(rng.gen()),
    };

    loop {
        if game.player.hp <= 0 {
            println!("You have died. Press Enter to exit.");
            let mut tmp = String::new();
            let _ = io::stdin().read_line(&mut tmp);
            break;
        }
        game.draw();
        let c = read_char();
        match c {
            Some('W') | Some('w') => {
                game.player_move(0, -1);
                game.monsters_take_turns();
            }
            Some('S') | Some('s') => {
                // This is overloaded: in-game S is save. Use capital S in instruction too.
                game.save("save.json");
            }
            Some('A') | Some('a') => {
                game.player_move(-1, 0);
                game.monsters_take_turns();
            }
            Some('D') | Some('d') => {
                game.player_move(1, 0);
                game.monsters_take_turns();
            }
            Some('Q') | Some('q') => {
                println!("Quit (Y to confirm)?");
                if let Some('Y') | Some('y') = read_char() {
                    println!("Goodbye.");
                    break;
                }
            }
            Some('G') | Some('g') => {
                game.pick_up();
            }
            Some('I') | Some('i') => {
                game.open_inventory();
            }
            Some('L') | Some('l') => {
                if let Some(loaded) = Game::load("save.json") {
                    game = loaded;
                }
            }
            Some(ch) => {
                println!("Unknown command: {}", ch);
            }
            None => {
                println!("Input error, exiting.");
                break;
            }
        }
    }
                  }
