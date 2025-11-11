#!/usr/bin/env python3
"""
main.py: Terminal menu to select and launch one of 20 games.
"""

import subprocess

def main():
    games = [
        ("Snake", "snake.py"),
        ("Minesweeper", "minesweeper.py"),
        ("Space Shooter", "shooter.py"),
        ("Pong", "pong.py"),
        ("Breakout", "breakout.py"),
        ("Flappy Bird", "flappy_bird.py"),
        ("Tic-Tac-Toe", "tic_tac_toe.py"),
        ("Connect Four", "connect_four.py"),
        ("Memory Match", "memory.py"),
        ("Simon Says", "simon.py"),
        ("Maze Runner", "maze_runner.py"),
        ("Catch Falling", "catch_falling.py"),
        ("Racing", "racing.py"),
        ("Platformer", "platformer.py"),
        ("Frogger", "frogger.py"),
        ("Space Invaders", "space_invaders.py"),
        ("Asteroid Avoider", "asteroids.py"),
        ("Whack-a-Mole", "whack_a_mole.py"),
        ("Balloon Pop", "balloon_pop.py")
    ]

    print("Pygame Games")
    for i, (name, _) in enumerate(games, start=1):
        print(f"{i}. {name}")
    choice = input("Enter game number (or 0 to quit): ")
    try:
        idx = int(choice) - 1
        if idx == -1:
            print("Goodbye!")
            return
        if 0 <= idx < len(games):
            _, script = games[idx]
            print(f"Launching {games[idx][0]}...")
            # Launch the selected game in a new process
            # This uses subprocess to call the Python interpreter on the game script:contentReference[oaicite:9]{index=9}.
            subprocess.run(['python3', script])
        else:
            print("Invalid choice.")
    except ValueError:
        print("Invalid input; please enter a number.")

if __name__ == "__main__":
    main()
