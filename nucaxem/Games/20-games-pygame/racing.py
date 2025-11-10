#!/usr/bin/env python3
"""
racing.py: Simple top-down racing. Dodge incoming cars. Left/Right to move.
"""

import pygame, random
from pygame.locals import QUIT, KEYDOWN, KEYUP, K_LEFT, K_RIGHT

WIDTH, HEIGHT = 300, 500
ROAD_WIDTH = 200
ROAD_LEFT = (WIDTH - ROAD_WIDTH) // 2
CAR_WIDTH = 30
CAR_HEIGHT = 50

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Racing")
    clock = pygame.time.Clock()

    player = pygame.Rect(WIDTH//2-CAR_WIDTH//2, HEIGHT-100, CAR_WIDTH, CAR_HEIGHT)
    speed = 0
    obstacles = []
    SPAWN = pygame.USEREVENT + 1
    pygame.time.set_timer(SPAWN, 1500)
    score = 0
    font = pygame.font.Font(None, 24)
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            elif event.type == SPAWN:
                lane = random.choice([ROAD_LEFT+20, ROAD_LEFT+ROAD_WIDTH-CAR_WIDTH-20])
                obstacles.append(pygame.Rect(lane, -CAR_HEIGHT, CAR_WIDTH, CAR_HEIGHT))
            elif event.type == KEYDOWN:
                if event.key == K_LEFT: speed = -5
                if event.key == K_RIGHT: speed = 5
            elif event.type == KEYUP:
                if event.key in (K_LEFT, K_RIGHT): speed = 0

        player.x += speed
        player.x = max(min(player.x, ROAD_LEFT+ROAD_WIDTH-CAR_WIDTH), ROAD_LEFT)

        for obs in obstacles[:]:
            obs.y += 5
            if obs.colliderect(player):
                print("Crashed!")
                running = False
            elif obs.top > HEIGHT:
                obstacles.remove(obs)
                score += 1

        screen.fill((0,128,0))  # grass
        pygame.draw.rect(screen, (50,50,50), (ROAD_LEFT, 0, ROAD_WIDTH, HEIGHT))
        pygame.draw.rect(screen, (255,255,255), (ROAD_LEFT+ROAD_WIDTH//2-5, 0, 10, HEIGHT))
        pygame.draw.rect(screen, (255,0,0), player)
        for obs in obstacles:
            pygame.draw.rect(screen, (0,0,255), obs)
        text = font.render("Score: " + str(score), True, (255,255,255))
        screen.blit(text, (10,10))
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()
