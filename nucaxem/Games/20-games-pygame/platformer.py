#!/usr/bin/env python3
"""
platformer.py: Simple platformer. Move with arrows and jump with space.
"""

import pygame
from pygame.locals import QUIT, KEYDOWN, KEYUP, K_LEFT, K_RIGHT, K_SPACE

WIDTH, HEIGHT = 400, 300
FPS = 60

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.rect = pygame.Rect(50, HEIGHT-60, 30, 40)
        self.vel_y = 0
    def update(self, keys, platforms):
        dx = 0
        if keys[K_LEFT]: dx = -5
        if keys[K_RIGHT]: dx = 5
        self.rect.x += dx
        # Gravity
        self.vel_y += 0.5
        self.rect.y += int(self.vel_y)
        # Check collisions with platforms
        for p in platforms:
            if self.rect.colliderect(p) and self.vel_y > 0:
                self.rect.bottom = p.top
                self.vel_y = 0
        # Floor
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT
            self.vel_y = 0

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Platformer")
    clock = pygame.time.Clock()

    player = Player()
    platforms = [pygame.Rect(0, HEIGHT-20, WIDTH, 20),
                 pygame.Rect(100, 200, 100, 10),
                 pygame.Rect(250, 150, 100, 10)]
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            elif event.type == KEYDOWN:
                if event.key == K_SPACE and player.vel_y == 0:
                    player.vel_y = -10  # jump
        keys = pygame.key.get_pressed()
        player.update(keys, platforms)

        screen.fill((135,206,235))
        pygame.draw.rect(screen, (255,0,0), player.rect)  # player
        for p in platforms:
            pygame.draw.rect(screen, (0,255,0), p)  # platforms green
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    main()
