import math
import os
import sys
import tty
import termios
import time

# colors lmao
RESET = "\033[0m"
CEILING_COLOR = "\033[38;5;240m"
FLOOR_COLOR = "\033[38;5;236m"

def wall_color(distance):
    if distance < 2:
        return "\033[38;5;196m"  # red
    elif distance < 4:
        return "\033[38;5;208m"  # orange
    elif distance < 6:
        return "\033[38;5;226m"  # yellow
    elif distance < 8:
        return "\033[38;5;118m"  # green
    elif distance < 12:
        return "\033[38;5;39m"   # blue
    else:
        return "\033[38;5;240m"  # gray

# map obviously you can read it under me
game_map = [
    "########################################",
    "#...............#......................#",
    "#..######.......#...........########...#",
    "#...............#......................#",
    "#...........##########.................#",
    "#.................................#....#",
    "#......#########..................#....#",
    "#....................#####........#....#",
    "#.........................#............#",
    "#...........######........#............#",
    "#.........................#............#",
    "#....#....................#............#",
    "#....#..........###########............#",
    "#....#.................................#",
    "#....#########.........................#",
    "#......................................#",
    "#......................######..........#",
    "#......................................#",
    "#..........################............#",
    "#......................................#",
    "########################################"
]

MAP_WIDTH = len(game_map[0])
MAP_HEIGHT = len(game_map)

# player shit
player_x = 3.5
player_y = 3.5
player_angle = 0.0

FOV = math.pi / 3
MAX_DEPTH = 20
SCREEN_WIDTH = 100
SCREEN_HEIGHT = 30

MOVE_SPEED = 0.25
TURN_SPEED = 0.12

# helpers because it wouldnt work properly
def get_key():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(fd)
        return sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

def clear_screen():
    os.system("clear")

# main game loop 
while True:
    screen_buffer = [""] * SCREEN_HEIGHT

    for col in range(SCREEN_WIDTH):
        ray_angle = (player_angle - FOV / 2) + (col / SCREEN_WIDTH) * FOV
        distance = 0
        hit_wall = False

        eye_x = math.cos(ray_angle)
        eye_y = math.sin(ray_angle)

        while not hit_wall and distance < MAX_DEPTH:
            distance += 0.05
            test_x = int(player_x + eye_x * distance)
            test_y = int(player_y + eye_y * distance)

            if test_x < 0 or test_x >= MAP_WIDTH or test_y < 0 or test_y >= MAP_HEIGHT:
                hit_wall = True
                distance = MAX_DEPTH
            elif game_map[test_y][test_x] == "#":
                hit_wall = True

        ceiling = int(SCREEN_HEIGHT / 2 - SCREEN_HEIGHT / distance)
        floor = SCREEN_HEIGHT - ceiling
        col_color = wall_color(distance)

        for row in range(SCREEN_HEIGHT):
            if row < ceiling:
                screen_buffer[row] += CEILING_COLOR + " " + RESET
            elif ceiling <= row <= floor:
                if distance <= MAX_DEPTH / 4:
                    shade = "█"
                elif distance < MAX_DEPTH / 3:
                    shade = "▓"
                elif distance < MAX_DEPTH / 2:
                    shade = "▒"
                else:
                    shade = "░"
                screen_buffer[row] += col_color + shade + RESET
            else:
                screen_buffer[row] += FLOOR_COLOR + "·" + RESET

    clear_screen()
    for line in screen_buffer:
        print(line)

    print("\nControls: W/S = move, A/D = turn, Q = quit")

    key = get_key().lower()

    if key == "q":
        break
    elif key == "a":
        player_angle -= TURN_SPEED
    elif key == "d":
        player_angle += TURN_SPEED
    elif key == "w":
        new_x = player_x + math.cos(player_angle) * MOVE_SPEED
        new_y = player_y + math.sin(player_angle) * MOVE_SPEED
        if game_map[int(new_y)][int(new_x)] != "#":
            player_x, player_y = new_x, new_y
    elif key == "s":
        new_x = player_x - math.cos(player_angle) * MOVE_SPEED
        new_y = player_y - math.sin(player_angle) * MOVE_SPEED
        if game_map[int(new_y)][int(new_x)] != "#":
            player_x, player_y = new_x, new_y

    time.sleep(0.01) # ezRefresh
