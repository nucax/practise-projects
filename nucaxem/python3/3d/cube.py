import curses
import math
import time

# ===============================
# 3D Math
# ===============================

def rotate_x(point, angle):
    x, y, z = point
    cos_a = math.cos(angle)
    sin_a = math.sin(angle)
    return (
        x,
        y * cos_a - z * sin_a,
        y * sin_a + z * cos_a
    )

def rotate_y(point, angle):
    x, y, z = point
    cos_a = math.cos(angle)
    sin_a = math.sin(angle)
    return (
        x * cos_a + z * sin_a,
        y,
        -x * sin_a + z * cos_a
    )

def rotate_z(point, angle):
    x, y, z = point
    cos_a = math.cos(angle)
    sin_a = math.sin(angle)
    return (
        x * cos_a - y * sin_a,
        x * sin_a + y * cos_a,
        z
    )

def project(point, width, height, fov, viewer_distance):
    x, y, z = point
    factor = fov / (viewer_distance + z)
    x = x * factor + width / 2
    y = -y * factor + height / 2
    return int(x), int(y)

# ===============================
# Cube Data
# ===============================

vertices = [
    (-1, -1, -1),
    (1, -1, -1),
    (1, 1, -1),
    (-1, 1, -1),
    (-1, -1, 1),
    (1, -1, 1),
    (1, 1, 1),
    (-1, 1, 1),
]

edges = [
    (0,1),(1,2),(2,3),(3,0),
    (4,5),(5,6),(6,7),(7,4),
    (0,4),(1,5),(2,6),(3,7)
]

# ===============================
# Bresenham Line Drawing
# ===============================

def draw_line(stdscr, x1, y1, x2, y2, char="#"):
    dx = abs(x2 - x1)
    dy = abs(y2 - y1)
    sx = 1 if x1 < x2 else -1
    sy = 1 if y1 < y2 else -1
    err = dx - dy

    while True:
        try:
            stdscr.addch(y1, x1, char)
        except:
            pass

        if x1 == x2 and y1 == y2:
            break

        e2 = 2 * err
        if e2 > -dy:
            err -= dy
            x1 += sx
        if e2 < dx:
            err += dx
            y1 += sy

# ===============================
# Engine Loop
# ===============================

def main(stdscr):
    curses.curs_set(0)
    stdscr.nodelay(True)
    stdscr.timeout(0)

    width = curses.COLS
    height = curses.LINES

    angle_x = angle_y = angle_z = 0
    camera = [0, 0, -5]

    fov = 200
    viewer_distance = 4

    while True:
        stdscr.clear()

        key = stdscr.getch()

        # Movement
        if key == ord('w'):
            camera[2] += 0.2
        if key == ord('s'):
            camera[2] -= 0.2
        if key == ord('a'):
            camera[0] -= 0.2
        if key == ord('d'):
            camera[0] += 0.2
        if key == ord('q'):
            camera[1] += 0.2
        if key == ord('e'):
            camera[1] -= 0.2
        if key == 27:
            break

        projected_points = []

        for vertex in vertices:
            rotated = rotate_x(vertex, angle_x)
            rotated = rotate_y(rotated, angle_y)
            rotated = rotate_z(rotated, angle_z)

            # Apply camera
            translated = (
                rotated[0] - camera[0],
                rotated[1] - camera[1],
                rotated[2] - camera[2],
            )

            if translated[2] == 0:
                translated = (translated[0], translated[1], 0.0001)

            projected = project(translated, width, height, fov, viewer_distance)
            projected_points.append(projected)

        for edge in edges:
            p1 = projected_points[edge[0]]
            p2 = projected_points[edge[1]]
            draw_line(stdscr, p1[0], p1[1], p2[0], p2[1])

        angle_x += 0.02
        angle_y += 0.03
        angle_z += 0.01

        stdscr.refresh()
        time.sleep(0.016)

curses.wrapper(main)
