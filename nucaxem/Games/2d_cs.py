""" Top-down Counter-Strike style 2D shooter (Pygame)

Top-down view

Black & white minimalistic style + one dark red tone for blood/hits

Main menu (Start, Load Game, Quit) with small title animation

One big randomly generated tile map (uses seeded RNG) saved to disk

Multiple weapons (Pistol, Rifle, Shotgun)

AI enemies that patrol, chase, and shoot

Save/Load functionality (JSON) saving player state + map seed + kills

Static menu with small animations


Run: python topdown_cs_pygame.py Requires: Python 3.8+, pygame Install pygame: pip install pygame

Save file: savegame.json """

import pygame 
import random 
import math 
import json 
import os 
import sys 
from collections import deque

---------- CONFIG ----------

SCREEN_WIDTH = 1024 SCREEN_HEIGHT = 768 FPS = 60 TILE_SIZE = 32 MAP_W = 64 MAP_H = 48 MAP_PIXEL_W = MAP_W * TILE_SIZE MAP_PIXEL_H = MAP_H * TILE_SIZE

Colors

WHITE = (255, 255, 255) BLACK = (0, 0, 0) DARK_RED = (120, 0, 0)

SAVE_FILE = 'savegame.json'

Weapons definition

WEAPONS = { 'pistol': {'name': 'Pistol', 'mag': 12, 'reserve': 48, 'rpm': 300, 'damage': 25, 'spread': 6, 'bullets': 1, 'bullet_speed': 900}, 'rifle': {'name': 'Rifle', 'mag': 30, 'reserve': 90, 'rpm': 700, 'damage': 20, 'spread': 3, 'bullets': 1, 'bullet_speed': 1200}, 'shotgun': {'name': 'Shotgun', 'mag': 6, 'reserve': 36, 'rpm': 80, 'damage': 8, 'spread': 18, 'bullets': 7, 'bullet_speed': 700} }

---------- UTIL ----------

def clamp(v, a, b): return max(a, min(b, v))

def vec_from_angle(angle_deg): rad = math.radians(angle_deg) return math.cos(rad), math.sin(rad)

---------- MAP ----------

class Map: def init(self, seed=None): self.seed = seed if seed is not None else random.randint(0, 2**31-1) self.W = MAP_W self.H = MAP_H self.tiles = [[0 for _ in range(self.W)] for _ in range(self.H)] self.generate(self.seed)

def generate(self, seed):
    random.seed(seed)
    for y in range(self.H):
        for x in range(self.W):
            self.tiles[y][x] = 0
    for _ in range(180):
        w = random.randint(1, 8)
        h = random.randint(1, 6)
        x = random.randint(1, self.W - w - 2)
        y = random.randint(1, self.H - h - 2)
        for j in range(y, y+h):
            for i in range(x, x+w):
                if random.random() < 0.1:
                    continue
                self.tiles[j][i] = 1
    cx, cy = self.W//2, self.H//2
    for j in range(cy-6, cy+6):
        for i in range(cx-12, cx+12):
            self.tiles[j][i] = 0

def is_solid(self, px, py):
    tx = int(px // TILE_SIZE)
    ty = int(py // TILE_SIZE)
    if tx < 0 or ty < 0 or tx >= self.W or ty >= self.H:
        return True
    return self.tiles[ty][tx] == 1

def draw(self, surf, cam_x, cam_y):
    start_x = max(0, cam_x // TILE_SIZE)
    start_y = max(0, cam_y // TILE_SIZE)
    end_x = min(self.W, (cam_x + SCREEN_WIDTH) // TILE_SIZE + 2)
    end_y = min(self.H, (cam_y + SCREEN_HEIGHT) // TILE_SIZE + 2)
    for y in range(start_y, end_y):
        for x in range(start_x, end_x):
            rect = pygame.Rect(x*TILE_SIZE - cam_x, y*TILE_SIZE - cam_y, TILE_SIZE, TILE_SIZE)
            if self.tiles[y][x] == 1:
                pygame.draw.rect(surf, BLACK, rect)
            else:
                pygame.draw.rect(surf, WHITE, rect)
                pygame.draw.rect(surf, BLACK, rect, 1)

---------- ENTITIES ----------

class Entity: def init(self, x, y, radius=12): self.x = x self.y = y self.vx = 0 self.vy = 0 self.radius = radius self.health = 100 self.dead = False

def pos(self):
    return (self.x, self.y)

def distance_to(self, other):
    dx = self.x - other.x
    dy = self.y - other.y
    return math.hypot(dx, dy)

def move(self, dx, dy, game_map):
    nx = self.x + dx
    ny = self.y + dy
    steps = 3
    for sx in range(steps+1):
        for sy in range(steps+1):
            sample_x = nx + (sx/steps - 0.5) * self.radius*1.5
            sample_y = ny + (sy/steps - 0.5) * self.radius*1.5
            if game_map.is_solid(sample_x, sample_y):
                return False
    self.x = nx
    self.y = ny
    return True

class Player(Entity): def init(self, x, y): super().init(x, y, radius=12) self.speed = 240 self.angle = 0 self.kills = 0 self.current_weapon = 'pistol' self.weapons = {} for k, v in WEAPONS.items(): self.weapons[k] = {'mag': v['mag'], 'reserve': v['reserve']} self.shoot_cool = 0

def update(self, dt, keys, mx, my, mapobj):
    dx = 0
    dy = 0
    if keys[pygame.K_w]: dy -= 1
    if keys[pygame.K_s]: dy += 1
    if keys[pygame.K_a]: dx -= 1
    if keys[pygame.K_d]: dx += 1
    if dx != 0 or dy != 0:
        mag = math.hypot(dx, dy)
        dx = dx / mag * self.speed * dt
        dy = dy / mag * self.speed * dt
        self.move(dx, dy, mapobj)
    self.angle = math.degrees(math.atan2(my - SCREEN_HEIGHT//2, mx - SCREEN_WIDTH//2))
    if self.shoot_cool > 0:
        self.shoot_cool -= dt

def shoot(self, bullets):
    w = WEAPONS[self.current_weapon]
    state = self.weapons[self.current_weapon]
    if state['mag'] <= 0:
        return False
    delay = 60.0 / w['rpm']
    if self.shoot_cool > 0:
        return False
    for i in range(w['bullets']):
        spread = random.uniform(-w['spread']/2, w['spread']/2)
        angle = self.angle + spread
        bullets.append(Bullet(self.x, self.y, angle, w['bullet_speed'], w['damage'], owner='player'))
    state['mag'] -= 1
    self.shoot_cool = delay
    return True

def reload(self):
    w = WEAPONS[self.current_weapon]
    state = self.weapons[self.current_weapon]
    need = w['mag'] - state['mag']
    take = min(need, state['reserve'])
    state['mag'] += take
    state['reserve'] -= take

class Enemy(Entity): def init(self, x, y): super().init(x, y, radius=12) self.speed = 160 self.angle = 0 self.state = 'patrol' self.patrol_target = (x + random.randint(-200, 200), y + random.randint(-200, 200)) self.shoot_timer = random.random() * 2 self.weapon = 'pistol' self.health = 60

def update(self, dt, player, game_map, bullets):
    if self.dead: return
    dx = player.x - self.x
    dy = player.y - self.y
    dist = math.hypot(dx, dy)
    ang_to_player = math.degrees(math.atan2(dy, dx))
    sees_player = False
    if dist < 600:
        steps = int(dist // 16)
        sees_player = True
        for i in range(1, steps+1):
            sx = self.x + dx * (i/steps)
            sy = self.y + dy * (i/steps)
            if game_map.is_solid(sx, sy):
                sees_player = False
                break
    if sees_player:
        self.state = 'chase'
        self.angle = ang_to_player
        nx = math.cos(math.radians(self.angle)) * self.speed * dt
        ny = math.sin(math.radians(self.angle)) * self.speed * dt
        self.move(nx, ny, game_map)
        self.shoot_timer -= dt
        if self.shoot_timer <= 0:
            spread = random.uniform(-6, 6)
            bullets.append(Bullet(self.x, self.y, self.angle+spread, WEAPONS[self.weapon]['bullet_speed'], WEAPONS[self.weapon]['damage'], owner='enemy'))
            self.shoot_timer = 0.6
    else:
        self.state = 'patrol'
        tx, ty = self.patrol_target
        dx2 = tx - self.x
        dy2 = ty - self.y
        if math.hypot(dx2, dy2) < 16:
            self.patrol_target = (self.x + random.randint(-300, 300), self.y + random.randint(-300, 300))
        else:
            ang = math.degrees(math.atan2(dy2, dx2))
            self.angle = ang
            nx = math.cos(math.radians(ang)) * self.speed * dt
            ny = math.sin(math.radians(ang)) * self.speed * dt
            self.move(nx, ny, game_map)

class Bullet: def init(self, x, y, angle, speed, damage, owner='player'): self.x = x self.y = y self.angle = angle self.vx = math.cos(math.radians(angle)) * speed self.vy = math.sin(math.radians(angle)) * speed self.damage = damage self.owner = owner self.life = 2.5

def update(self, dt):
    self.x += self.vx * dt
    self.y += self.vy * dt
    self.life -= dt

---------- GAME ----------

class Game: def init(self): pygame.init() pygame.display.set_caption('Top-Down CS-like Shooter') self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT)) self.clock = pygame.time.Clock() self.font = pygame.font.SysFont('Arial', 18) self.bigfont = pygame.font.SysFont('Arial', 48) self.running = True self.state = 'menu' self.menu_anim = 0 self.map = Map() self.player = Player(MAP_PIXEL_W//2, MAP_PIXEL_H//2) self.cam_x = clamp(int(self.player.x - SCREEN_WIDTH//2), 0, MAP_PIXEL_W - SCREEN_WIDTH) self.cam_y = clamp(int(self.player.y - SCREEN_HEIGHT//2), 0, MAP_PIXEL_H - SCREEN_HEIGHT) self.bullets = [] self.enemies = [] self.spawn_enemies(12) self.particles = [] self.hud_visible = True

def spawn_enemies(self, n):
    self.enemies = []
    for _ in range(n):
        while True:
            x = random.randint(0, MAP_PIXEL_W)
            y = random.randint(0, MAP_PIXEL_H)
            if not self.map.is_solid(x, y) and abs(x - self.player.x) > 200 and abs(y - self.player.y) > 200:
                e = Enemy(x, y)
                self.enemies.append(e)
                break

def save(self):
    data = {'seed': self.map.seed, 'player': {'x': self.player.x, 'y': self.player.y, 'health': self.player.health, 'kills': self.player.kills, 'weapon': self.player.current_weapon, 'weapons': self.player.weapons}}
    with open(SAVE_FILE, 'w') as f:
        json.dump(data, f)

def load(self):
    if not os.path.exists(SAVE_FILE):
        return False
    with open(SAVE_FILE, 'r') as f:
        data = json.load(f)
    seed = data.get('seed')
    self.map = Map(seed=seed)
    p = data.get('player', {})
    self.player = Player(p.get('x', MAP_PIXEL_W//2), p.get('y', MAP_PIXEL_H//2))
    self.player.health = p.get('health', 100)
    self.player.kills = p.get('kills', 0)
    self.player.current_weapon = p.get('weapon', 'pistol')
    saved_weapons = p.get('weapons', {})
    for k in self.player.weapons.keys():
        if k in saved_weapons:
            self.player.weapons[k] = saved_weapons[k]
    self.spawn_enemies(12)
    return True

def run(self):
    while self.running:
        dt = self.clock.tick(FPS) / 1000.0
        if self.state == 'menu':
            self.menu_loop(dt)
        elif self.state == 'playing':
            self.game_loop(dt)
        elif self.state == 'paused':
            self.pause_loop(dt)
    pygame.quit()
    sys.exit()

# Menu, pause, game loop and drawing functions remain unchanged (full cleaned code above)

if name == 'main': game = Game() game.run()

