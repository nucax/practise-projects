#!/usr/bin/env python3
"""
minesweeper.py: Simple Minesweeper. Click squares to reveal, avoid mines. Right-click to flag (optional).
"""

import pygame, random
from pygame.locals import QUIT, MOUSEBUTTONDOWN

# Settings
WIDTH, HEIGHT = 300, 300
ROWS, COLS = 10, 10
CELL_SIZE = WIDTH // COLS
MINES_COUNT = 10

def create_board():
    """Create a board with mines and numbers."""
    board = [[0 for _ in range(COLS)] for _ in range(ROWS)]
    # Place mines
    mines = random.sample(range(ROWS*COLS), MINES_COUNT)
    for m in mines:
        r, c = divmod(m, COLS)
        board[r][c] = -1
    # Calculate numbers
    for r in range(ROWS):
        for c in range(COLS):
            if board[r][c] == -1: continue
            # count adjacent mines
            count = 0
            for dr in (-1,0,1):
                for dc in (-1,0,1):
                    rr, cc = r+dr, c+dc
                    if 0 <= rr < ROWS and 0 <= cc < COLS and board[rr][cc] == -1:
                        count += 1
            board[r][c] = count
    return board

def draw_board(screen, board, revealed):
    """Draw the Minesweeper grid. Hidden = gray, revealed white or number/mine."""
    for r in range(ROWS):
        for c in range(COLS):
            rect = pygame.Rect(c*CELL_SIZE, r*CELL_SIZE, CELL_SIZE, CELL_SIZE)
            if (r,c) not in revealed:
                pygame.draw.rect(screen, (192,192,192), rect)  # gray hidden
            else:
                if board[r][c] == -1:
                    pygame.draw.rect(screen, (255, 0, 0), rect)  # red for mine
                else:
                    pygame.draw.rect(screen, (255, 255, 255), rect)  # white
                    if board[r][c] > 0:
                        # draw number
                        font = pygame.font.Font(None, 24)
                        text = font.render(str(board[r][c]), True, (0,0,0))
                        screen.blit(text, (c*CELL_SIZE+5, r*CELL_SIZE+5))
            pygame.draw.rect(screen, (0,0,0), rect, 1)  # border

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Minesweeper")
    clock = pygame.time.Clock()

    board = create_board()
    revealed = set()  # set of (r,c) revealed
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            elif event.type == MOUSEBUTTONDOWN:
                mx, my = event.pos
                row = my // CELL_SIZE
                col = mx // CELL_SIZE
                if 0 <= row < ROWS and 0 <= col < COLS:
                    if board[row][col] == -1:
                        # Hit a mine: game over
                        running = False
                    else:
                        revealed.add((row, col))
                        # Reveal neighbors if zero (flood fill)
                        if board[row][col] == 0:
                            stack = [(row, col)]
                            while stack:
                                r, c = stack.pop()
                                for dr in (-1,0,1):
                                    for dc in (-1,0,1):
                                        rr, cc = r+dr, c+dc
                                        if 0 <= rr < ROWS and 0 <= cc < COLS:
                                            if (rr,cc) not in revealed and board[rr][cc] != -1:
                                                revealed.add((rr,cc))
                                                if board[rr][cc] == 0:
                                                    stack.append((rr,cc))

        screen.fill((0, 0, 0))
        draw_board(screen, board, revealed)
        pygame.display.flip()
        clock.tick(30)

    pygame.quit()

if __name__ == "__main__":
    main()
