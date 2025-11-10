#!/usr/bin/env python3
"""
flappy_bird.py: Flappy Bird clone. Press SPACE to flap and avoid pipes.
"""

import pygame, random
from pygame.locals import QUIT, KEYDOWN, K_SPACE

WIDTH, HEIGHT = 400, 600
PIPE_WIDTH = 50
GAP = 150

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Flappy Bird")
    clock = pygame.time.Clock()

    # Bird
    bird = pygame.Rect(50, HEIGHT//2, 30, 30)
    bird_vel = 0
    gravity = 0.5

    # Pipes: list of (x, gap_y)
    pipes = []
    SPAWNPIPE = pygame.USEREVENT + 1
    pygame.time.set_timer(SPAWNPIPE, 1500)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            elif event.type == KEYDOWN and event.key == K_SPACE:
                bird_vel = -10  # flap
            elif event.type == SPAWNPIPE:
                gap_y = random.randint(100, HEIGHT - 100 - GAP)
                pipes.append(pygame.Rect(WIDTH, 0, PIPE_WIDTH, gap_y))
                pipes.append(pygame.Rect(WIDTH, gap_y+GAP, PIPE_WIDTH, HEIGHT-(gap_y+GAP)))

        # Bird physics
        bird_vel += gravity
        bird.y += int(bird_vel)
        # Bounds check
        if bird.top <= 0: bird.top = 0
        if bird.bottom >= HEIGHT: running = False

        # Move pipes
        for pipe in pipes:
            pipe.x -= 3
        # Remove off-screen pipes
        pipes = [p for p in pipes if p.right > 0]

        # Check collisions
        for pipe in pipes:
            if bird.colliderect(pipe):
                running = False

        # Draw
        screen.fill((135, 206, 235))  # sky blue
        pygame.draw.ellipse(screen, (255,255,0), bird)  # bird as yellow circle
        for pipe in pipes:
            pygame.draw.rect(screen, (34, 139, 34), pipe)  # pipes as green
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()
