#!/usr/bin/env python3
"""
memory.py: Memory match game. Click cards to reveal colors, match pairs.
"""

import pygame, random
from pygame.locals import QUIT, MOUSEBUTTONDOWN

ROWS, COLS = 4, 4
WIDTH, HEIGHT = 400, 400
CARD_SIZE = WIDTH // COLS

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Memory Match")
    clock = pygame.time.Clock()

    # Create pairs of colors
    colors = [(255,0,0), (0,255,0), (0,0,255), (255,255,0),
              (255,165,0), (128,0,128), (0,255,255), (255,192,203)]
    colors = colors[:ROWS*COLS//2] * 2
    random.shuffle(colors)

    board = [colors[i*COLS:(i+1)*COLS] for i in range(ROWS)]
    revealed = [[False]*COLS for _ in range(ROWS)]
    first = None  # first card chosen
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            elif event.type == MOUSEBUTTONDOWN:
                mx, my = event.pos
                r, c = my//CARD_SIZE, mx//CARD_SIZE
                if 0 <= r < ROWS and 0 <= c < COLS and not revealed[r][c]:
                    revealed[r][c] = True
                    if first is None:
                        first = (r,c)
                    else:
                        r0,c0 = first
                        # If not matching, hide again after short delay
                        if board[r][c] != board[r0][c0]:
                            pygame.time.wait(500)
                            revealed[r][c] = revealed[r0][c0] = False
                        first = None

        screen.fill((0,0,0))
        # Draw cards
        for r in range(ROWS):
            for c in range(COLS):
                rect = pygame.Rect(c*CARD_SIZE, r*CARD_SIZE, CARD_SIZE-5, CARD_SIZE-5)
                if revealed[r][c]:
                    pygame.draw.rect(screen, board[r][c], rect)
                else:
                    pygame.draw.rect(screen, (169,169,169), rect)
        pygame.display.flip()
        clock.tick(30)

    pygame.quit()

if __name__ == "__main__":
    main()
