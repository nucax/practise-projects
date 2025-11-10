#!/usr/bin/env python3
"""
balloon_pop.py: Balloon Pop. Shoot (click) ascending balloons.
"""

import pygame, random
from pygame.locals import QUIT, MOUSEBUTTONDOWN

WIDTH, HEIGHT = 400, 400

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Balloon Pop")
    clock = pygame.time.Clock()

    balloons = []
    SPAWN = pygame.USEREVENT + 1
    pygame.time.set_timer(SPAWN, 800)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            elif event.type == SPAWN:
                x = random.randint(50, WIDTH-50)
                balloons.append(pygame.Rect(x, HEIGHT, 30, 40))
            elif event.type == MOUSEBUTTONDOWN:
                for b in balloons[:]:
                    if b.collidepoint(event.pos):
                        balloons.remove(b)
                        print("Popped!")
        for b in balloons:
            b.y -= 2
            # Draw string
        screen.fill((135,206,250))
        for b in balloons:
            pygame.draw.ellipse(screen, (255,0,0), b)  # balloon red
            pygame.draw.line(screen, (0,0,0), (b.centerx, b.bottom), (b.centerx, b.bottom+10), 2)
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()
