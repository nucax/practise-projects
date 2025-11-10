#!/usr/bin/env python3
"""
space_invaders.py: Space Invaders. Move ship with arrows, shoot aliens with spacebar.
"""

import pygame, random
from pygame.locals import QUIT, KEYDOWN, K_LEFT, K_RIGHT, K_SPACE

WIDTH, HEIGHT = 400, 600

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Space Invaders")
    clock = pygame.time.Clock()

    # Player ship
    player = pygame.Rect(WIDTH//2-20, HEIGHT-50, 40, 20)
    player_speed = 5
    bullets = []
    # Aliens: a grid
    aliens = []
    rows, cols = 5, 8
    for r in range(rows):
        for c in range(cols):
            aliens.append(pygame.Rect(50+c*40, 50+r*30, 30, 20))
    alien_dir = 1  # 1=right, -1=left

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == QUIT: running = False
            elif event.type == KEYDOWN:
                if event.key == K_SPACE:
                    bullets.append(pygame.Rect(player.centerx, player.top, 3, 10))
        keys = pygame.key.get_pressed()
        if keys[K_LEFT] and player.left > 0: player.x -= player_speed
        if keys[K_RIGHT] and player.right < WIDTH: player.x += player_speed

        # Update bullets
        for b in bullets[:]:
            b.y -= 10
            if b.bottom < 0: bullets.remove(b)
        # Update aliens
        move_down = False
        for alien in aliens:
            alien.x += 2 * alien_dir
            if alien.right >= WIDTH or alien.left <= 0:
                move_down = True
        if move_down:
            alien_dir *= -1
            for alien in aliens:
                alien.y += 10

        # Check collisions
        for b in bullets[:]:
            for alien in aliens[:]:
                if b.colliderect(alien):
                    bullets.remove(b)
                    aliens.remove(alien)
                    break

        screen.fill((0,0,0))
        pygame.draw.rect(screen, (0,255,0), player)
        for b in bullets: pygame.draw.rect(screen, (255,255,0), b)
        for alien in aliens: pygame.draw.rect(screen, (255,0,0), alien)
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()
