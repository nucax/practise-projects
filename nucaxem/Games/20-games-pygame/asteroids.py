#!/usr/bin/env python3
"""
asteroids.py: Asteroid Avoider. Dodge falling asteroids. Left/Right to move the spaceship.
"""

import pygame, random
from pygame.locals import QUIT, KEYDOWN, KEYUP, K_LEFT, K_RIGHT

WIDTH, HEIGHT = 400, 500

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Asteroid Avoider")
    clock = pygame.time.Clock()

    ship = pygame.Rect(WIDTH//2-15, HEIGHT-60, 30, 30)
    speed = 0
    asteroids = []
    spawn_asteroid = pygame.USEREVENT + 1
    pygame.time.set_timer(spawn_asteroid, 800)
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == QUIT: running = False
            elif event.type == spawn_asteroid:
                x = random.randint(0, WIDTH-20)
                asteroids.append(pygame.Rect(x, 0, 20, 20))
            elif event.type == KEYDOWN:
                if event.key == K_LEFT: speed = -5
                if event.key == K_RIGHT: speed = 5
            elif event.type == KEYUP:
                if event.key in (K_LEFT, K_RIGHT): speed = 0

        ship.x += speed
        ship.x = max(min(ship.x, WIDTH-ship.width), 0)
        for a in asteroids[:]:
            a.y += 5
            if a.colliderect(ship):
                print("Crashed!")
                running = False
            elif a.top > HEIGHT:
                asteroids.remove(a)
        screen.fill((0,0,0))
        pygame.draw.polygon(screen, (0,255,255), [(ship.x, ship.bottom), (ship.x+ship.width/2, ship.top), (ship.x+ship.width, ship.bottom)])  # simple ship
        for a in asteroids:
            pygame.draw.circle(screen, (128,128,128), a.center, 10)
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()
