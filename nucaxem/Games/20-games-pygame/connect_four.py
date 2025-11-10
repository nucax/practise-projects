#!/usr/bin/env python3
"""
connect_four.py: Two-player Connect Four. Click a column to drop a piece.
"""

import pygame
from pygame.locals import QUIT, MOUSEBUTTONDOWN

ROWS, COLS = 6, 7
SQUARE_SIZE = 60
WIDTH = COLS * SQUARE_SIZE
HEIGHT = (ROWS+1) * SQUARE_SIZE  # extra row for drop
RADIUS = SQUARE_SIZE//2 - 5

def create_board():
    return [["" for _ in range(COLS)] for _ in range(ROWS)]

def draw_board(screen, board):
    # Draw board background
    for r in range(ROWS):
        for c in range(COLS):
            pygame.draw.rect(screen, (0,0,255), (c*SQUARE_SIZE, (r+1)*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
            color = (255,255,255)
            if board[ROWS-1-r][c] == "R": color = (255,0,0)
            elif board[ROWS-1-r][c] == "Y": color = (255,255,0)
            pygame.draw.circle(screen, color, (c*SQUARE_SIZE+SQUARE_SIZE//2, (r+1)*SQUARE_SIZE+SQUARE_SIZE//2), RADIUS)
    pygame.display.update()

def winning_move(board, piece):
    # Check horizontal, vertical, diagonal wins
    for c in range(COLS-3):
        for r in range(ROWS):
            if all(board[r][c+i] == piece for i in range(4)): return True
    for c in range(COLS):
        for r in range(ROWS-3):
            if all(board[r+i][c] == piece for i in range(4)): return True
    for c in range(COLS-3):
        for r in range(ROWS-3):
            if all(board[r+i][c+i] == piece for i in range(4)): return True
    for c in range(COLS-3):
        for r in range(3, ROWS):
            if all(board[r-i][c+i] == piece for i in range(4)): return True
    return False

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Connect Four")
    font = pygame.font.Font(None, 36)
    board = create_board()
    turn = 0  # 0=Red, 1=Yellow
    game_over = False
    draw_board(screen, board)

    while not game_over:
        for event in pygame.event.get():
            if event.type == QUIT:
                game_over = True
            elif event.type == MOUSEBUTTONDOWN:
                x = event.pos[0]
                col = x // SQUARE_SIZE
                if col < COLS and board[ROWS-1][col] == "":
                    for row in range(ROWS):
                        if board[row][col] == "":
                            board[row][col] = "R" if turn == 0 else "Y"
                            break
                    if winning_move(board, "R" if turn == 0 else "Y"):
                        print(f"{'Red' if turn==0 else 'Yellow'} wins!")
                        game_over = True
                    turn ^= 1  # switch player
                    draw_board(screen, board)
        clock = pygame.time.Clock()
        clock.tick(30)

    pygame.quit()

if __name__ == "__main__":
    main()
