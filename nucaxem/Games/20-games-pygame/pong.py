#!/usr/bin/env python3
"""
pong.py: Classic Pong. Two paddles, a bouncing ball. Player 1 = A/Z keys, Player 2 = K/M keys.
"""

import pygame
from pygame.locals import QUIT, KEYDOWN, KEYUP, K_w, K_s, K_UP, K_DOWN

WIDTH, HEIGHT = 400, 300
PADDLE_WIDTH, PADDLE_HEIGHT = 10, 50
BALL_SIZE = 10

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Pong")
    clock = pygame.time.Clock()

    # Paddles
    paddle1 = pygame.Rect(10, HEIGHT//2 - PADDLE_HEIGHT//2, PADDLE_WIDTH, PADDLE_HEIGHT)
    paddle2 = pygame.Rect(WIDTH-20, HEIGHT//2 - PADDLE_HEIGHT//2, PADDLE_WIDTH, PADDLE_HEIGHT)
    speed1 = speed2 = 0
    # Ball
    ball = pygame.Rect(WIDTH//2, HEIGHT//2, BALL_SIZE, BALL_SIZE)
    ball_speed = [3, 3]

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            elif event.type == KEYDOWN:
                if event.key == K_w: speed1 = -5
                if event.key == K_s: speed1 = 5
                if event.key == K_UP: speed2 = -5
                if event.key == K_DOWN: speed2 = 5
            elif event.type == KEYUP:
                if event.key in (K_w, K_s): speed1 = 0
                if event.key in (K_UP, K_DOWN): speed2 = 0

        # Move paddles
        paddle1.y += speed1
        paddle2.y += speed2
        paddle1.y = max(min(paddle1.y, HEIGHT-PADDLE_HEIGHT), 0)
        paddle2.y = max(min(paddle2.y, HEIGHT-PADDLE_HEIGHT), 0)

        # Move ball
        ball.x += ball_speed[0]
        ball.y += ball_speed[1]
        # Bounce off top/bottom
        if ball.top <= 0 or ball.bottom >= HEIGHT:
            ball_speed[1] = -ball_speed[1]
        # Bounce off paddles
        if ball.colliderect(paddle1) or ball.colliderect(paddle2):
            ball_speed[0] = -ball_speed[0]

        # Reset if out of bounds
        if ball.left <= 0 or ball.right >= WIDTH:
            ball.center = (WIDTH//2, HEIGHT//2)

        # Draw
        screen.fill((0,0,0))
        pygame.draw.rect(screen, (255,255,255), paddle1)
        pygame.draw.rect(screen, (255,255,255), paddle2)
        pygame.draw.ellipse(screen, (255,255,255), ball)  # ball as white circle
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()
