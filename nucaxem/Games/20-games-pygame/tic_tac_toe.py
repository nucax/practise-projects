#!/usr/bin/env python3
"""
tic_tac_toe.py: Two-player Tic-Tac-Toe. Click cells to place X or O.
"""

import pygame
from pygame.locals import QUIT, MOUSEBUTTONDOWN

WIDTH, HEIGHT = 300, 300
GRID_SIZE = 3
CELL = WIDTH // GRID_SIZE

def draw_board(screen, board):
    screen.fill((255,255,255))
    # Draw grid lines
    for i in range(1, GRID_SIZE):
        pygame.draw.line(screen, (0,0,0), (0, i*CELL), (WIDTH, i*CELL), 2)
        pygame.draw.line(screen, (0,0,0), (i*CELL, 0), (i*CELL, HEIGHT), 2)
    # Draw X and O
    font = pygame.font.Font(None, 100)
    for r in range(GRID_SIZE):
        for c in range(GRID_SIZE):
            if board[r][c] != "":
                text = font.render(board[r][c], True, (0,0,0))
                rect = text.get_rect(center=(c*CELL+CELL//2, r*CELL+CELL//2))
                screen.blit(text, rect)

def check_win(board):
    # Check rows, columns, diagonals
    lines = board + [list(col) for col in zip(*board)]
    lines.append([board[i][i] for i in range(GRID_SIZE)])
    lines.append([board[i][GRID_SIZE-1-i] for i in range(GRID_SIZE)])
    for line in lines:
        if line.count(line[0]) == GRID_SIZE and line[0] != "":
            return True
    return False

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Tic-Tac-Toe")
    clock = pygame.time.Clock()

    board = [["" for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
    current = "X"
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            elif event.type == MOUSEBUTTONDOWN:
                mx, my = event.pos
                row, col = my//CELL, mx//CELL
                if 0 <= row < GRID_SIZE and 0 <= col < GRID_SIZE:
                    if board[row][col] == "":
                        board[row][col] = current
                        if check_win(board):
                            print(f"{current} wins!")
                            running = False
                        # Check draw
                        elif all(board[r][c] != "" for r in range(GRID_SIZE) for c in range(GRID_SIZE)):
                            print("Draw!")
                            running = False
                        else:
                            current = "O" if current == "X" else "X"

        draw_board(screen, board)
        pygame.display.flip()
        clock.tick(30)

    pygame.quit()

if __name__ == "__main__":
    main()
