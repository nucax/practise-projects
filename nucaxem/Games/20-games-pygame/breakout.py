#!/usr/bin/env python3
"""
breakout.py: Breakout/Brick Breaker. Bounce the ball to break bricks.
Left/Right arrows to move paddle.
"""

import pygame
from pygame.locals import QUIT, KEYDOWN, KEYUP, K_LEFT, K_RIGHT

WIDTH, HEIGHT = 400, 300
PADDLE_WIDTH, PADDLE_HEIGHT = 60, 10
BALL_SIZE = 8

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Breakout")
    clock = pygame.time.Clock()

    # Paddle
    paddle = pygame.Rect(WIDTH//2 - PADDLE_WIDTH//2, HEIGHT-30, PADDLE_WIDTH, PADDLE_HEIGHT)
    paddle_speed = 0
    # Ball
    ball = pygame.Rect(WIDTH//2, HEIGHT//2, BALL_SIZE, BALL_SIZE)
    ball_speed = [3, -3]
    # Bricks: a grid of rectangles
    bricks = []
    rows, cols = 5, 7
    brick_width = WIDTH // cols
    brick_height = 20
    for row in range(rows):
        for col in range(cols):
            brick = pygame.Rect(col*brick_width, row*brick_height, brick_width-2, brick_height-2)
            bricks.append(brick)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            elif event.type == KEYDOWN:
                if event.key == K_LEFT: paddle_speed = -5
                if event.key == K_RIGHT: paddle_speed = 5
            elif event.type == KEYUP:
                if event.key in (K_LEFT, K_RIGHT): paddle_speed = 0

        paddle.x += paddle_speed
        paddle.x = max(min(paddle.x, WIDTH-PADDLE_WIDTH), 0)

        ball.x += ball_speed[0]
        ball.y += ball_speed[1]
        # Bounce off walls
        if ball.left <= 0 or ball.right >= WIDTH:
            ball_speed[0] = -ball_speed[0]
        if ball.top <= 0:
            ball_speed[1] = -ball_speed[1]
        # Bounce off paddle
        if ball.colliderect(paddle) and ball_speed[1] > 0:
            ball_speed[1] = -ball_speed[1]
        # Bounce off bricks
        hit_index = ball.collidelist(bricks)
        if hit_index != -1:
            hit_brick = bricks.pop(hit_index)
            ball_speed[1] = -ball_speed[1]

        # Reset if ball misses paddle
        if ball.bottom >= HEIGHT:
            ball.x, ball.y = WIDTH//2, HEIGHT//2
            ball_speed = [3, -3]

        # Draw
        screen.fill((0,0,0))
        pygame.draw.rect(screen, (200,200,200), paddle)
        pygame.draw.ellipse(screen, (255,255,255), ball)
        for brick in bricks:
            pygame.draw.rect(screen, (0,128,255), brick)
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()
