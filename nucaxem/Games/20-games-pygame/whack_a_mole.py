#!/usr/bin/env python3
"""
whack_a_mole.py: Whack-a-Mole. Click the mole (red square) before it moves.
"""

import pygame, random
from pygame.locals import QUIT, MOUSEBUTTONDOWN

WIDTH, HEIGHT = 300, 300
HOLES = [(50,50), (150,50), (250,50),
         (50,150), (150,150), (250,150),
         (50,250), (150,250), (250,250)]

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Whack-a-Mole")
    clock = pygame.time.Clock()

    mole_index = random.randrange(len(HOLES))
    mole_rect = pygame.Rect(HOLES[mole_index][0], HOLES[mole_index][1], 40, 40)
    timer = 0
    interval = 1000  # milliseconds

    running = True
    while running:
        dt = clock.tick(60)
        timer += dt
        if timer > interval:
            timer = 0
            mole_index = random.randrange(len(HOLES))
            mole_rect = pygame.Rect(HOLES[mole_index][0], HOLES[mole_index][1], 40, 40)

        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            elif event.type == MOUSEBUTTONDOWN:
                if mole_rect.collidepoint(event.pos):
                    print("Hit!")
                    running = False

        screen.fill((0,128,0))
        # Draw holes
        for pos in HOLES:
            pygame.draw.rect(screen, (139,69,19), (pos[0], pos[1], 40, 40))
        # Draw mole
        pygame.draw.rect(screen, (255,0,0), mole_rect)
        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()
