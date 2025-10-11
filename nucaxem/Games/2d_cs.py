""" Top-down Counter-Strike style 2D shooter (Pygame) Features:

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

import pygame import random import math import json import os import sys from collections import deque

---------- CONFIG ----------

SCREEN_WIDTH = 1024 SCREEN_HEIGHT = 768 FPS = 60 TILE_SIZE = 32 MAP_W = 64  # tiles MAP_H = 48 MAP_PIXEL_W = MAP_W * TILE_SIZE MAP_PIXEL_H = MAP_H * TILE_SIZE

Colors (black & white + dark red tone)

WHITE = (255, 255, 255) BLACK = (0, 0, 0) DARK_RED = (120, 0, 0)

SAVE_FILE = 'savegame.json'

Weapons definition

WEAPONS = { 'pistol': { 'name': 'Pistol', 'mag': 12, 'reserve': 48, 'rpm': 300, 'damage': 25, 'spread': 6, 'bullets': 1, 'bullet_speed': 900 }, 'rifle': { 'name': 'Rifle', 'mag': 30, 'reserve': 90, 'rpm': 700, 'damage': 20, 'spread': 3, 'bullets': 1, 'bullet_speed': 1200 }, 'shotgun': { 'name': 'Shotgun', 'mag': 6, 'reserve': 36, 'rpm': 80, 'damage': 8, 'spread': 18, 'bullets': 7, 'bullet_speed': 700 } }

---------- UTIL ----------

def clamp(v, a, b): return max(a, min(b, v))

def vec_from_angle(angle_deg): rad = math.radians(angle_deg) return math.cos(rad), math.sin(rad)

---------- MAP ----------

class Map: def init(self, seed=None): self.seed = seed if seed is not None else random.randint(0, 2**31-1) self.W = MAP_W self.H = MAP_H self.tiles = [[0 for _ in range(self.W)] for _ in range(self.H)] self.generate(self.seed)

def generate(self, seed):
    random.seed(seed)
    # Fill with floor(0) then carve rooms/walls
    for y in range(self.H):
        for x in range(self.W):
            self.tiles[y][x] = 0
    # place some rectangular walls randomly
    for _ in range(180):
        w = random.randint(1, 8)
        h = random.randint(1, 6)
        x = random.randint(1, self.W - w - 2)
        y = random.randint(1, self.H - h - 2)
        for j in range(y, y+h):
            for i in range(x, x+w):
                # occasional gaps
                if random.random() < 0.1:
                    continue
                self.tiles[j][i] = 1
    # carve bigger central arena
    cx, cy = self.W//2, self.H//2
    for j in range(cy-6, cy+6):
        for i in range(cx-12, cx+12):
            self.tiles[j][i] = 0

def is_solid(self, px, py):
    # px,py in pixels
    tx = int(px // TILE_SIZE)
    ty = int(py // TILE_SIZE)
    if tx < 0 or ty < 0 or tx >= self.W or ty >= self.H:
        return True
    return self.tiles[ty][tx] == 1

def draw(self, surf, cam_x, cam_y):
    # draw visible tile range
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
                # subtle grid lines
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
    # simple collision with solid tiles
    nx = self.x + dx
    ny = self.y + dy
    # check four sample points around circle
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

class Player(Entity): def init(self, x, y): super().init(x, y, radius=12) self.speed = 240 self.angle = 0 self.kills = 0 # weapon state self.current_weapon = 'pistol' self.weapons = {} for k, v in WEAPONS.items(): self.weapons[k] = {'mag': v['mag'], 'reserve': v['reserve']} self.shoot_cool = 0

def update(self, dt, keys, mx, my, mapobj):
    # movement
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
    # angle to mouse
    self.angle = math.degrees(math.atan2(my - SCREEN_HEIGHT//2, mx - SCREEN_WIDTH//2))
    if self.shoot_cool > 0:
        self.shoot_cool -= dt

def shoot(self, bullets):
    w = WEAPONS[self.current_weapon]
    state = self.weapons[self.current_weapon]
    if state['mag'] <= 0:
        return False
    rpm = w['rpm']
    delay = 60.0 / rpm
    if self.shoot_cool > 0:
        return False
    # spawn bullets
    for i in range(w['bullets']):
        spread = random.uniform(-w['spread']/2, w['spread']/2)
        angle = self.angle + spread
        bx = self.x
        by = self.y
        speed = w['bullet_speed']
        bullets.append(Bullet(bx, by, angle, speed, w['damage'], owner='player'))
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
    if self.dead:
        return
    # simple LOS
    dx = player.x - self.x
    dy = player.y - self.y
    dist = math.hypot(dx, dy)
    ang_to_player = math.degrees(math.atan2(dy, dx))
    sees_player = False
    if dist < 600:
        # raycast by sampling
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
        # move toward player
        nx = math.cos(math.radians(self.angle)) * self.speed * dt
        ny = math.sin(math.radians(self.angle)) * self.speed * dt
        self.move(nx, ny, game_map)
        # shooting
        self.shoot_timer -= dt
        if self.shoot_timer <= 0:
            # fire a bullet with some spread
            spread = random.uniform(-6, 6)
            bullets.append(Bullet(self.x, self.y, self.angle+spread, WEAPONS[self.weapon]['bullet_speed'], WEAPONS[self.weapon]['damage'], owner='enemy'))
            self.shoot_timer = 0.6
    else:
        # patrol
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

class Game: def init(self): pygame.init() pygame.display.set_caption('Top-Down CS-like Shooter') self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT)) self.clock = pygame.time.Clock() self.font = pygame.font.SysFont('Arial', 18) self.bigfont = pygame.font.SysFont('Arial', 48) self.running = True # menu state self.state = 'menu' self.menu_anim = 0 # create or load map self.map = Map() # center spawn sx = MAP_PIXEL_W//2 sy = MAP_PIXEL_H//2 self.player = Player(sx, sy) self.cam_x = clamp(int(self.player.x - SCREEN_WIDTH//2), 0, MAP_PIXEL_W - SCREEN_WIDTH) self.cam_y = clamp(int(self.player.y - SCREEN_HEIGHT//2), 0, MAP_PIXEL_H - SCREEN_HEIGHT) self.bullets = [] self.enemies = [] self.spawn_enemies(12) self.particles = [] # UI self.hud_visible = True

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
    data = {
        'seed': self.map.seed,
        'player': {
            'x': self.player.x, 'y': self.player.y, 'health': self.player.health,
            'kills': self.player.kills, 'weapon': self.player.current_weapon,
            'weapons': self.player.weapons
        }
    }
    with open(SAVE_FILE, 'w') as f:
        json.dump(data, f)
    print('Saved to', SAVE_FILE)

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
    # restore mags
    saved_weapons = p.get('weapons', {})
    for k in self.player.weapons.keys():
        if k in saved_weapons:
            self.player.weapons[k] = saved_weapons[k]
    self.spawn_enemies(12)
    print('Loaded save from', SAVE_FILE)
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

# ---------- MENU ----------
def menu_loop(self, dt):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            self.running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mx, my = pygame.mouse.get_pos()
            # buttons
            if 420 <= mx <= 600 and 340 <= my <= 380:
                # Start New
                self.map = Map()
                self.player = Player(MAP_PIXEL_W//2, MAP_PIXEL_H//2)
                self.spawn_enemies(12)
                self.bullets = []
                self.state = 'playing'
            if 420 <= mx <= 600 and 400 <= my <= 440:
                # Load
                if self.load():
                    self.bullets = []
                    self.state = 'playing'
            if 420 <= mx <= 600 and 460 <= my <= 500:
                self.running = False
    # menu animation
    self.menu_anim += dt
    pulse = 1.0 + 0.06 * math.sin(self.menu_anim * 2.0)
    # draw
    self.screen.fill(WHITE)
    title_surf = self.bigfont.render('BLACK OPS', True, BLACK)
    title_rect = title_surf.get_rect(center=(SCREEN_WIDTH//2, 180))
    # pulsing shadow for slight animation
    shadow = pygame.Surface((title_rect.w+40, title_rect.h+20))
    shadow.fill(WHITE)
    self.screen.blit(title_surf, title_rect)
    # buttons
    btns = [('Start New', 340), ('Load Game', 400), ('Quit', 460)]
    for text, y in btns:
        rect = pygame.Rect(420, y, 180, 40)
        pygame.draw.rect(self.screen, BLACK, rect, 2)
        txt = self.font.render(text, True, BLACK)
        self.screen.blit(txt, (rect.x + 10, rect.y + 10))
    # small credits
    cred = self.font.render('Top-down CS-like shooter — black & white + dark red', True, BLACK)
    self.screen.blit(cred, (10, SCREEN_HEIGHT - 30))
    pygame.display.flip()

# ---------- PAUSE ----------
def pause_loop(self, dt):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            self.running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.state = 'playing'
    # draw paused overlay
    self.draw_world()
    overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 120))
    self.screen.blit(overlay, (0, 0))
    txt = self.bigfont.render('PAUSED', True, WHITE)
    r = txt.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
    self.screen.blit(txt, r)
    pygame.display.flip()

# ---------- GAME LOOP ----------
def game_loop(self, dt):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            self.running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.state = 'paused'
            elif event.key == pygame.K_r:
                self.player.reload()
            elif event.key == pygame.K_1:
                self.player.current_weapon = 'pistol'
            elif event.key == pygame.K_2:
                self.player.current_weapon = 'rifle'
            elif event.key == pygame.K_3:
                self.player.current_weapon = 'shotgun'
            elif event.key == pygame.K_F5:
                self.save()
            elif event.key == pygame.K_F9:
                if os.path.exists(SAVE_FILE):
                    os.remove(SAVE_FILE)
            elif event.key == pygame.K_F1:
                self.hud_visible = not self.hud_visible
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                mx, my = pygame.mouse.get_pos()
                # shoot
                # convert mouse pos to world coordinates
                wx = self.cam_x + mx
                wy = self.cam_y + my
                self.player.angle = math.degrees(math.atan2(wy - self.player.y, wx - self.player.x))
                self.player.shoot(self.bullets)
            elif event.button == 3:
                # reload on right click for convenience
                self.player.reload()
    keys = pygame.key.get_pressed()
    mx, my = pygame.mouse.get_pos()
    # update player
    self.player.update(dt, keys, mx, my, self.map)
    # update bullets
    for b in list(self.bullets):
        b.update(dt)
        # collide with walls
        if self.map.is_solid(b.x, b.y) or b.life <= 0 or b.x < 0 or b.y < 0 or b.x > MAP_PIXEL_W or b.y > MAP_PIXEL_H:
            self.bullets.remove(b)
            continue
        # hit entities
        if b.owner == 'player':
            for e in self.enemies:
                if not e.dead and math.hypot(b.x - e.x, b.y - e.y) < e.radius:
                    e.health -= b.damage
                    self.bullets.remove(b)
                    self.particles.append((e.x, e.y, 0.4))
                    if e.health <= 0:
                        e.dead = True
                        self.player.kills += 1
                    break
        else:
            # enemy bullet can hit player
            if math.hypot(b.x - self.player.x, b.y - self.player.y) < self.player.radius:
                self.player.health -= b.damage
                self.bullets.remove(b)
                self.particles.append((self.player.x, self.player.y, 0.4))
                if self.player.health <= 0:
                    self.player.dead = True
                continue
    # update enemies
    for e in self.enemies:
        if not e.dead:
            e.update(dt, self.player, self.map, self.bullets)
    # remove dead enemies after some time
    # update particles
    new_particles = []
    for x, y, t in self.particles:
        t -= dt
        if t > 0:
            new_particles.append((x, y, t))
    self.particles = new_particles
    # camera follow
    self.cam_x = clamp(int(self.player.x - SCREEN_WIDTH//2), 0, MAP_PIXEL_W - SCREEN_WIDTH)
    self.cam_y = clamp(int(self.player.y - SCREEN_HEIGHT//2), 0, MAP_PIXEL_H - SCREEN_HEIGHT)
    # draw
    self.draw_world()
    pygame.display.flip()

def draw_world(self):
    # background
    self.screen.fill(WHITE)
    # map
    self.map.draw(self.screen, self.cam_x, self.cam_y)
    # draw bullets
    for b in self.bullets:
        bx = int(b.x - self.cam_x)
        by = int(b.y - self.cam_y)
        pygame.draw.circle(self.screen, BLACK, (bx, by), 2)
    # draw enemies
    for e in self.enemies:
        ex = int(e.x - self.cam_x)
        ey = int(e.y - self.cam_y)
        if e.dead:
            # corpse darker red
            pygame.draw.circle(self.screen, DARK_RED, (ex, ey), e.radius)
            continue
        pygame.draw.circle(self.screen, BLACK, (ex, ey), e.radius)
        # eyes as white dots showing facing
        fx = int(ex + math.cos(math.radians(e.angle)) * 6)
        fy = int(ey + math.sin(math.radians(e.angle)) * 6)
        pygame.draw.circle(self.screen, WHITE, (fx, fy), 3)
    # draw player at center
    center = (SCREEN_WIDTH//2, SCREEN_HEIGHT//2)
    pygame.draw.circle(self.screen, BLACK, center, self.player.radius)
    # muzzle direction
    fx = int(center[0] + math.cos(math.radians(self.player.angle)) * 18)
    fy = int(center[1] + math.sin(math.radians(self.player.angle)) * 18)
    pygame.draw.line(self.screen, WHITE, center, (fx, fy), 3)
    # draw particle hits in dark red
    for x, y, t in self.particles:
        sx = int(x - self.cam_x)
        sy = int(y - self.cam_y)
        alpha = int(255 * (t / 0.4))
        surf = pygame.Surface((6, 6), pygame.SRCALPHA)
        surf.fill((DARK_RED[0], DARK_RED[1], DARK_RED[2], alpha))
        self.screen.blit(surf, (sx-3, sy-3))
    # draw HUD
    if self.hud_visible:
        self.draw_hud()

def draw_hud(self):
    # HUD background
    pygame.draw.rect(self.screen, WHITE, (8, 8, 300, 120))
    pygame.draw.rect(self.screen, BLACK, (8, 8, 300, 120), 2)
    # health
    htxt = self.font.render(f'Health: {int(self.player.health)}', True, BLACK)
    self.screen.blit(htxt, (16, 16))
    # weapon info
    w = WEAPONS[self.player.current_weapon]
    st = self.player.weapons[self.player.current_weapon]
    wtxt = self.font.render(f"{w['name']}  Mag: {st['mag']} / {w['mag']}  Reserve: {st['reserve']}", True, BLACK)
    self.screen.blit(wtxt, (16, 40))
    ktxt = self.font.render(f'Kills: {self.player.kills}', True, BLACK)
    self.screen.blit(ktxt, (16, 64))
    inst = self.font.render('1-3: switch  R: reload  F5: save  Esc: pause', True, BLACK)
    self.screen.blit(inst, (16, 92))

if name == 'main': game = Game() game.run()
