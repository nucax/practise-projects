use crossterm::{
    cursor, event::{self, Event, KeyCode}, terminal::{self, ClearType}, ExecutableCommand,
};
use std::collections::VecDeque;
use std::io::{stdout, Write};
use std::thread;
use std::time::{Duration, Instant};

const WIDTH: usize = 60;
const HEIGHT: usize = 20;
const FPS: u64 = 60;
const MAX_SPEED: f32 = 1.5;
const ACCEL: f32 = 0.05;
const FRICTION: f32 = 0.02;
const TURN_SPEED: f32 = 0.05;
const NITRO_BOOST: f32 = 0.05;
const LAP_COUNT: usize = 3;

#[derive(Clone, Copy)]
struct Vec2 {
    x: f32,
    y: f32,
}

impl Vec2 {
    fn new(x: f32, y: f32) -> Self { Self { x, y } }
    fn add(&self, o: Vec2) -> Vec2 { Vec2::new(self.x + o.x, self.y + o.y) }
    fn mul(&self, s: f32) -> Vec2 { Vec2::new(self.x * s, self.y * s) }
}

#[derive(Clone)]
struct Car {
    pos: Vec2,
    vel: Vec2,
    dir: f32,
    glyph: char,
    name: String,
    laps: usize,
    checkpoint: usize,
    nitro: f32,
}

impl Car {
    fn new(x: f32, y: f32, glyph: char, name: &str) -> Self {
        Self {
            pos: Vec2::new(x, y),
            vel: Vec2::new(0.0, 0.0),
            dir: 0.0,
            glyph,
            name: name.to_string(),
            laps: 0,
            checkpoint: 0,
            nitro: 0.0,
        }
    }
}

struct Track {
    grid: Vec<Vec<char>>,
    checkpoints: Vec<Vec2>,
}

impl Track {
    fn new() -> Self {
        let mut grid = vec![vec![' '; WIDTH]; HEIGHT];
        for y in 0..HEIGHT {
            for x in 0..WIDTH {
                if y == 0 || y == HEIGHT - 1 || x == 0 || x == WIDTH - 1 {
                    grid[y][x] = '#';
                }
            }
        }
        // example track: rectangle with checkpoints
        let checkpoints = vec![
            Vec2::new(5.0, 1.0),
            Vec2::new(WIDTH as f32 - 6.0, 1.0),
            Vec2::new(WIDTH as f32 - 6.0, HEIGHT as f32 - 2.0),
            Vec2::new(5.0, HEIGHT as f32 - 2.0),
        ];
        Self { grid, checkpoints }
    }

    fn draw(&self, cars: &[Car]) {
        let mut buffer = self.grid.clone();
        for car in cars {
            let x = car.pos.x as usize;
            let y = car.pos.y as usize;
            if x < WIDTH && y < HEIGHT {
                buffer[y][x] = car.glyph;
            }
        }
        stdout()
            .execute(cursor::MoveTo(0, 0))
            .unwrap()
            .execute(terminal::Clear(ClearType::All))
            .unwrap();
        for row in buffer {
            println!("{}", row.iter().collect::<String>());
        }
    }

    fn check_collision(&self, pos: Vec2) -> bool {
        let x = pos.x as usize;
        let y = pos.y as usize;
        if x >= WIDTH || y >= HEIGHT { return true; }
        self.grid[y][x] == '#'
    }

    fn check_checkpoint(&self, car: &mut Car) {
        if car.checkpoint < self.checkpoints.len() {
            let cp = self.checkpoints[car.checkpoint];
            if ((car.pos.x - cp.x).abs() < 1.0) && ((car.pos.y - cp.y).abs() < 1.0) {
                car.checkpoint += 1;
                if car.checkpoint >= self.checkpoints.len() {
                    car.checkpoint = 0;
                    car.laps += 1;
                }
            }
        }
    }
}

fn main() {
    terminal::enable_raw_mode().unwrap();
    stdout().execute(cursor::Hide).unwrap();

    let mut track = Track::new();
    let mut player = Car::new(5.0, 2.0, '@', "Player");
    let mut ai1 = Car::new(6.0, 2.0, 'A', "AI1");
    let mut ai2 = Car::new(7.0, 2.0, 'B', "AI2");

    let mut cars = vec![player.clone(), ai1.clone(), ai2.clone()];
    let mut last_frame = Instant::now();
    let mut running = true;

    while running {
        // input
        while event::poll(Duration::from_millis(1)).unwrap() {
            if let Event::Key(k) = event::read().unwrap() {
                match k.code {
                    KeyCode::Char('q') => running = false,
                    KeyCode::Char('w') => {
                        let accel = ACCEL + player.nitro;
                        player.vel.x += player.dir.cos() * accel;
                        player.vel.y += player.dir.sin() * accel;
                    }
                    KeyCode::Char('s') => {
                        player.vel.x *= 0.9;
                        player.vel.y *= 0.9;
                    }
                    KeyCode::Char('a') => { player.dir -= TURN_SPEED; }
                    KeyCode::Char('d') => { player.dir += TURN_SPEED; }
                    KeyCode::Char('n') => {
                        if player.nitro < 0.3 { player.nitro += NITRO_BOOST; }
                    }
                    _ => {}
                }
            }
        }

        // physics update
        if last_frame.elapsed() >= Duration::from_millis(1000 / FPS) {
            for car in &mut cars {
                car.pos = car.pos.add(car.vel);
                car.vel = car.vel.mul(1.0 - FRICTION);
                if track.check_collision(car.pos) {
                    car.vel = car.vel.mul(-0.5);
                }
                track.check_checkpoint(car);
            }

            // simple AI: follow checkpoints
            for ai in &mut cars[1..] {
                let cp = track.checkpoints[ai.checkpoint];
                let dir_to_cp = (cp.y - ai.pos.y).atan2(cp.x - ai.pos.x);
                let angle_diff = dir_to_cp - ai.dir;
                ai.dir += angle_diff * 0.05;
                ai.vel.x += ai.dir.cos() * ACCEL * 0.5;
                ai.vel.y += ai.dir.sin() * ACCEL * 0.5;
            }

            track.draw(&cars);

            // leaderboard
            cars.sort_by(|a, b| b.laps.cmp(&a.laps));
            println!("Leaderboard:");
            for c in &cars {
                println!("{}: {} laps", c.name, c.laps);
            }

            // check victory
            if player.laps >= LAP_COUNT {
                println!("You won!");
                break;
            }

            last_frame = Instant::now();
        }
    }

    terminal::disable_raw_mode().unwrap();
    stdout().execute(cursor::Show).unwrap();
}
