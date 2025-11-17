use crossterm::{
    cursor,
    event::{self, Event, KeyCode},
    terminal::{self, ClearType},
    ExecutableCommand,
};
use std::cmp::{max, min};
use std::io::{stdout, Write};
use std::time::{Duration, Instant};

const WIDTH: usize = 80;
const HEIGHT: usize = 30;

const GRAVITY: f32 = 50.0;
const DT: f32 = 0.016; // 60 fps physics

#[derive(Clone, Copy)]
struct Vec2 {
    x: f32,
    y: f32,
}

impl Vec2 {
    fn new(x: f32, y: f32) -> Self {
        Self { x, y }
    }
    fn add(&self, o: Vec2) -> Vec2 {
        Vec2::new(self.x + o.x, self.y + o.y)
    }
    fn sub(&self, o: Vec2) -> Vec2 {
        Vec2::new(self.x - o.x, self.y - o.y)
    }
    fn mul(&self, s: f32) -> Vec2 {
        Vec2::new(self.x * s, self.y * s)
    }
}

#[derive(Clone)]
struct Particle {
    pos: Vec2,
    vel: Vec2,
    radius: f32,
}

#[derive(Clone)]
struct BoxBody {
    pos: Vec2,
    vel: Vec2,
    w: f32,
    h: f32,
}

enum Entity {
    Particle(Particle),
    Box(BoxBody),
}

struct World {
    entities: Vec<Entity>,
    running: bool,
}

impl World {
    fn new() -> Self {
        Self {
            entities: Vec::new(),
            running: true,
        }
    }

    fn spawn_particle(&mut self, x: f32, y: f32) {
        self.entities.push(Entity::Particle(Particle {
            pos: Vec2::new(x, y),
            vel: Vec2::new(0.0, 0.0),
            radius: 0.5,
        }));
    }

    fn spawn_box(&mut self, x: f32, y: f32, w: f32, h: f32) {
        self.entities.push(Entity::Box(BoxBody {
            pos: Vec2::new(x, y),
            vel: Vec2::new(0.0, 0.0),
            w,
            h,
        }));
    }

    fn step(&mut self) {
        for e in self.entities.iter_mut() {
            match e {
                Entity::Particle(p) => {
                    p.vel.y += GRAVITY * DT;
                    p.pos = p.pos.add(p.vel.mul(DT));
                    self.collide_particle(p);
                }
                Entity::Box(b) => {
                    b.vel.y += GRAVITY * DT;
                    b.pos = b.pos.add(b.vel.mul(DT));
                    self.collide_box(b);
                }
            }
        }

        // collisions between particles and boxes
        let len = self.entities.len();
        for i in 0..len {
            for j in i + 1..len {
                Self::resolve_collision(&mut self.entities[i], &mut self.entities[j]);
            }
        }
    }

    fn collide_particle(&self, p: &mut Particle) {
        if p.pos.y > HEIGHT as f32 - 1.0 {
            p.pos.y = HEIGHT as f32 - 1.0;
            p.vel.y *= -0.5;
        }
        if p.pos.x < 0.0 {
            p.pos.x = 0.0;
            p.vel.x *= -0.5;
        }
        if p.pos.x > WIDTH as f32 - 1.0 {
            p.pos.x = WIDTH as f32 - 1.0;
            p.vel.x *= -0.5;
        }
    }

    fn collide_box(&self, b: &mut BoxBody) {
        if b.pos.y + b.h > HEIGHT as f32 - 1.0 {
            b.pos.y = HEIGHT as f32 - 1.0 - b.h;
            b.vel.y *= -0.3;
        }
        if b.pos.x < 0.0 {
            b.pos.x = 0.0;
            b.vel.x *= -0.3;
        }
        if b.pos.x + b.w > WIDTH as f32 - 1.0 {
            b.pos.x = WIDTH as f32 - 1.0 - b.w;
            b.vel.x *= -0.3;
        }
    }

    fn resolve_collision(a: &mut Entity, b: &mut Entity) {
        match (a, b) {
            (Entity::Particle(pa), Entity::Particle(pb)) => {
                let diff = pb.pos.sub(pa.pos);
                let dist2 = diff.x * diff.x + diff.y * diff.y;

                if dist2 < 1.0 {
                    let normal = Vec2::new(diff.x, diff.y);
                    pa.vel.x -= normal.x * 0.5;
                    pa.vel.y -= normal.y * 0.5;
                    pb.vel.x += normal.x * 0.5;
                    pb.vel.y += normal.y * 0.5;
                }
            }

            (Entity::Particle(p), Entity::Box(bx)) |
            (Entity::Box(bx), Entity::Particle(p)) => {
                if p.pos.x > bx.pos.x &&
                   p.pos.x < bx.pos.x + bx.w &&
                   p.pos.y > bx.pos.y &&
                   p.pos.y < bx.pos.y + bx.h {

                    // push particle out upward
                    p.pos.y = bx.pos.y - 1.0;
                    p.vel.y *= -0.4;
                }
            }

            (Entity::Box(a), Entity::Box(b)) => {
                let ax2 = a.pos.x + a.w;
                let bx2 = b.pos.x + b.w;
                let ay2 = a.pos.y + a.h;
                let by2 = b.pos.y + b.h;

                if a.pos.x < bx2 && ax2 > b.pos.x &&
                   a.pos.y < by2 && ay2 > b.pos.y {

                    a.pos.y -= 1.0;
                    a.vel.y = -0.3;
                }
            }
        }
    }

    fn draw(&self) {
        let mut buffer = vec![vec![' '; WIDTH]; HEIGHT];

        for e in &self.entities {
            match e {
                Entity::Particle(p) => {
                    let x = p.pos.x as i32;
                    let y = p.pos.y as i32;
                    if x >= 0 && x < WIDTH as i32 && y >= 0 && y < HEIGHT as i32 {
                        buffer[y as usize][x as usize] = 'o';
                    }
                }
                Entity::Box(b) => {
                    for ix in 0..b.w as i32 {
                        for iy in 0..b.h as i32 {
                            let x = (b.pos.x as i32) + ix;
                            let y = (b.pos.y as i32) + iy;
                            if x >= 0 && x < WIDTH as i32 && y >= 0 && y < HEIGHT as i32 {
                                buffer[y as usize][x as usize] = '#';
                            }
                        }
                    }
                }
            }
        }

        stdout()
            .execute(cursor::MoveTo(0, 0))
            .unwrap()
            .execute(terminal::Clear(ClearType::All))
            .unwrap();

        for row in buffer {
            let line: String = row.into_iter().collect();
            println!("{}", line);
        }

        println!("Commands: [P]ause | [Space] spawn particle | [B] spawn box | [Q]uit");
    }
}

fn main() {
    terminal::enable_raw_mode().unwrap();
    stdout().execute(cursor::Hide).unwrap();

    let mut world = World::new();
    let mut last_frame = Instant::now();

    loop {
        // input
        if event::poll(Duration::from_millis(1)).unwrap() {
            if let Event::Key(k) = event::read().unwrap() {
                match k.code {
                    KeyCode::Char('q') => break,
                    KeyCode::Char('p') => world.running = !world.running,
                    KeyCode::Char(' ') => world.spawn_particle(40.0, 0.0),
                    KeyCode::Char('b') => world.spawn_box(38.0, 0.0, 4.0, 2.0),
                    _ => {}
                }
            }
        }

        // physics update
        if world.running && last_frame.elapsed() >= Duration::from_millis(16) {
            world.step();
            world.draw();
            last_frame = Instant::now();
        }
    }

    terminal::disable_raw_mode().unwrap();
    stdout().execute(cursor::Show).unwrap();
              }
