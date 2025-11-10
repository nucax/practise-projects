#!/usr/bin/env python3
"""
simon.py: Simon Says memory game. Repeat color sequences. Keys 1-4 for colors.
"""

import pygame, random
from pygame.locals import QUIT, KEYDOWN, K_1, K_2, K_3, K_4

WIDTH, HEIGHT = 400, 400
COLORS = [(255,0,0), (0,255,0), (0,0,255), (255,255,0)]  # red, green, blue, yellow
RECTS = [pygame.Rect(50,50,140,140), pygame.Rect(210,50,140,140),
         pygame.Rect(50,210,140,140), pygame.Rect(210,210,140,140)]

def flash(screen, index):
    """Flash a color block briefly."""
    pygame.draw.rect(screen, COLORS[index], RECTS[index])
    pygame.display.flip()
    pygame.time.wait(500)
    pygame.draw.rect(screen, (128,128,128), RECTS[index])
    pygame.display.flip()
    pygame.time.wait(200)

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Simon Says")
    for rect in RECTS:
        pygame.draw.rect(screen, (128,128,128), rect)
    pygame.display.flip()

    sequence = []
    running = True
    while running:
        # Add new color to sequence
        sequence.append(random.randrange(4))
        # Show sequence
        for idx in sequence:
            flash(screen, idx)
        # Player turn
        for idx in sequence:
            waiting = True
            while waiting:
                for event in pygame.event.get():
                    if event.type == QUIT:
                        running = False; waiting = False
                    elif event.type == KEYDOWN:
                        if event.key == K_1: choice = 0
                        elif event.key == K_2: choice = 1
                        elif event.key == K_3: choice = 2
                        elif event.key == K_4: choice = 3
                        else: continue
                        flash(screen, choice)
                        if choice != idx:
                            print("Wrong! Game over.")
                            running = False
                        waiting = False
                        break
                if not running: break
        if not running: break
    pygame.quit()

if __name__ == "__main__":
    main()
