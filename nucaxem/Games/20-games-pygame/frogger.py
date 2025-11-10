#!/usr/bin/env python3
"""
frogger.py: Frogger-like game. Move the frog with arrow keys to cross lanes avoiding cars.
"""

import pygame, random
from pygame.locals import QUIT, KEYDOWN, KEYUP, K_LEFT, K_RIGHT, K_UP, K_DOWN

WIDTH, HEIGHT = 400, 400
FROG_SIZE = 20

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Frogger")
    clock = pygame.time.Clock()

    frog = pygame.Rect(WIDTH//2, HEIGHT-40, FROG_SIZE, FROG_SIZE)
    cars = []
    lanes = [60, 120, 180, 240]
    SPEEDS = [2, -3, 4, -5]
    for lane, speed in zip(lanes, SPEEDS):
        # spawn initial cars
        for i in range(3):
            x = random.randrange(0, WIDTH, 100)
            cars.append(pygame.Rect(x, lane, 60, 20))
    move_x = move_y = 0
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == QUIT: running = False
            elif event.type == KEYDOWN:
                if event.key == K_LEFT: move_x = -5
                if event.key == K_RIGHT: move_x = 5
                if event.key == K_UP: move_y = -5
                if event.key == K_DOWN: move_y = 5
            elif event.type == KEYUP:
                if event.key in (K_LEFT, K_RIGHT): move_x = 0
                if event.key in (K_UP, K_DOWN): move_y = 0

        frog.x += move_x; frog.y += move_y
        frog.x = max(min(frog.x, WIDTH-FROG_SIZE), 0)
        frog.y = max(min(frog.y, HEIGHT-FROG_SIZE), 0)
        # Move cars
        for i, car in enumerate(cars):
            car.x += SPEEDS[i//3]  # 3 cars per lane
            # Wrap around
            if car.right < 0: car.left = WIDTH
            if car.left > WIDTH: car.right = 0
        # Check collision
        for car in cars:
            if frog.colliderect(car):
                print("You were hit! Game over.")
                running = False

        # Check win (reach top)
        if frog.top <= 0:
            print("You crossed the road! You win!")
            running = False

        screen.fill((0,200,0))  # grass background
        pygame.draw.rect(screen, (255,0,0), frog)
        for car in cars:
            pygame.draw.rect(screen, (0,0,255), car)
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()
