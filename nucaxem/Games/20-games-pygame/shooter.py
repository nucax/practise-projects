#!/usr/bin/env python3
"""
shooter.py: Simple 2D space shooter. Move with arrows, shoot with spacebar.
"""

import pygame, random
from pygame.locals import QUIT, KEYDOWN, K_LEFT, K_RIGHT, K_SPACE

WIDTH, HEIGHT = 400, 600

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.rect = pygame.Rect(WIDTH//2-20, HEIGHT-40, 40, 20)

    def update(self, keys):
        if keys[K_LEFT] and self.rect.left > 0:
            self.rect.x -= 5
        if keys[K_RIGHT] and self.rect.right < WIDTH:
            self.rect.x += 5

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.rect = pygame.Rect(x, y, 5, 10)

    def update(self):
        self.rect.y -= 10
        if self.rect.bottom < 0:
            self.kill()

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.rect = pygame.Rect(random.randrange(WIDTH-30), -30, 30, 20)
        self.speed = random.randint(2,5)
    def update(self):
        self.rect.y += self.speed
        if self.rect.top > HEIGHT:
            self.kill()

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Space Shooter")
    clock = pygame.time.Clock()

    player = Player()
    bullets = pygame.sprite.Group()
    enemies = pygame.sprite.Group()

    # Spawn enemy event
    SPAWNENEMY = pygame.USEREVENT + 1
    pygame.time.set_timer(SPAWNENEMY, 1000)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            elif event.type == SPAWNENEMY:
                enemies.add(Enemy())
            elif event.type == KEYDOWN:
                if event.key == K_SPACE:
                    # Shoot bullet from top of player
                    bullet = Bullet(player.rect.centerx, player.rect.top)
                    bullets.add(bullet)

        keys = pygame.key.get_pressed()
        player.update(keys)
        bullets.update()
        enemies.update()

        # Check collisions: bullet hits enemy
        for e in pygame.sprite.groupcollide(enemies, bullets, True, True).keys():
            pass  # remove both

        screen.fill((0, 0, 0))
        pygame.draw.rect(screen, (0, 255, 0), player.rect)  # player = green rectangle
        for b in bullets: pygame.draw.rect(screen, (255,255,0), b.rect)  # bullets = yellow
        for e in enemies: pygame.draw.rect(screen, (255,0,0), e.rect)   # enemies = red
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()
