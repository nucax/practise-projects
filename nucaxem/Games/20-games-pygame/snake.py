#!/usr/bin/env python3
"""
snake.py: A simple Snake game. Use arrow keys to move the snake and eat food.
"""

import pygame, random
from pygame.locals import QUIT, KEYDOWN, K_UP, K_DOWN, K_LEFT, K_RIGHT

# Game settings
WIDTH, HEIGHT = 400, 400
CELL_SIZE = 20
assert WIDTH % CELL_SIZE == 0 and HEIGHT % CELL_SIZE == 0
CELL_WIDTH = WIDTH // CELL_SIZE
CELL_HEIGHT = HEIGHT // CELL_SIZE

def draw_rect(surface, color, pos):
    """Draw one grid square at pos=(x,y) in cells."""
    rect = pygame.Rect(pos[0]*CELL_SIZE, pos[1]*CELL_SIZE, CELL_SIZE, CELL_SIZE)
    pygame.draw.rect(surface, color, rect)

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Snake")
    clock = pygame.time.Clock()

    # Initialize snake: list of (x,y) positions
    snake = [(CELL_WIDTH//2, CELL_HEIGHT//2)]
    direction = (1, 0)  # moving right
    # Place first food
    food = (random.randrange(CELL_WIDTH), random.randrange(CELL_HEIGHT))

    running = True
    while running:
        # Event handling
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            elif event.type == KEYDOWN:
                # Change direction; disallow reverse
                if event.key == K_UP and direction != (0,1):
                    direction = (0, -1)
                elif event.key == K_DOWN and direction != (0,-1):
                    direction = (0, 1)
                elif event.key == K_LEFT and direction != (1,0):
                    direction = (-1, 0)
                elif event.key == K_RIGHT and direction != (-1,0):
                    direction = (1, 0)

        # Move snake: add new head and remove tail
        head = snake[0]
        new_head = ((head[0] + direction[0]) % CELL_WIDTH,
                    (head[1] + direction[1]) % CELL_HEIGHT)
        # Check self-collision
        if new_head in snake:
            running = False  # game over
        else:
            snake.insert(0, new_head)
            if new_head == food:
                # Eat food: place new one
                food = (random.randrange(CELL_WIDTH), random.randrange(CELL_HEIGHT))
            else:
                snake.pop()  # move forward

        # Draw everything
        screen.fill((0, 0, 0))  # black background
        # Draw food
        draw_rect(screen, (255, 0, 0), food)  # red square
        # Draw snake
        for pos in snake:
            draw_rect(screen, (0, 255, 0), pos)  # green squares
        # Update display
        pygame.display.flip()
        clock.tick(10)  # 10 frames per second

    pygame.quit()

if __name__ == "__main__":
    main()
