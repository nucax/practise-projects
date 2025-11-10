#!/usr/bin/env python3
"""
maze_runner.py: Maze Runner. Navigate through a simple maze to reach the exit.
Arrow keys to move.
"""

import pygame
from pygame.locals import QUIT, KEYDOWN, K_UP, K_DOWN, K_LEFT, K_RIGHT

CELL = 40
MAZE = [
    "XXXXXXXXXXXXXXXXXXXX",
    "X  X       X       X",
    "X XX XXXX XXXXX XX X",
    "X                  X",
    "X XXXX XXXXXX XXXX X",
    "X X    X    X  X   X",
    "X X XXXX XX X  XXX X",
    "X X      XX        X",
    "X XXXXXX XX XXXXXX X",
    "X        XX       EX",
    "XXXXXXXXXXXXXXXXXXXX"
]

def main():
    rows = len(MAZE)
    cols = len(MAZE[0])
    WIDTH = cols * CELL
    HEIGHT = rows * CELL
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Maze Runner")
    clock = pygame.time.Clock()

    # Find start (S) or just set starting point
    player = pygame.Rect(CELL+5, CELL+5, CELL-10, CELL-10)  # assume start near top-left
    # Pre-draw maze layout surfaces
    wall_color = (0,0,0)
    floor_color = (200,200,200)
    exit_rect = None
    while True:
        # Draw Maze
        for r, row in enumerate(MAZE):
            for c, ch in enumerate(row):
                rect = pygame.Rect(c*CELL, r*CELL, CELL, CELL)
                if ch == "X":
                    pygame.draw.rect(screen, wall_color, rect)
                else:
                    pygame.draw.rect(screen, floor_color, rect)
                if ch == "E":
                    exit_rect = rect
                    pygame.draw.rect(screen, (0,255,0), rect)  # exit in green
        break

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            elif event.type == KEYDOWN:
                dx = dy = 0
                if event.key == K_UP: dy = -CELL
                if event.key == K_DOWN: dy = CELL
                if event.key == K_LEFT: dx = -CELL
                if event.key == K_RIGHT: dx = CELL
                # Move and check wall collision
                new_pos = player.move(dx, dy)
                # Check if hitting wall
                grid_x = new_pos.x // CELL
                grid_y = new_pos.y // CELL
                if 0 <= grid_y < rows and 0 <= grid_x < cols and MAZE[grid_y][grid_x] != "X":
                    player = new_pos

        # Check exit
        if exit_rect and player.colliderect(exit_rect):
            print("You reached the exit!")
            running = False

        # Redraw (floor already drawn, just draw player)
        pygame.draw.rect(screen, (255,0,0), player)  # player in red
        pygame.display.flip()
        clock.tick(30)

    pygame.quit()

if __name__ == "__main__":
    main()
