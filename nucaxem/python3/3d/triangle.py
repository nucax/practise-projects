# default env


# for drawing
import curses

# for building the cube
import math

# for showing
import time



# Math
def vec_sub(a, b):
    return (a[0]-b[0], a[1]-b[1], a[2]-b[2])




def vec_cross(a, b):
    return (
        a[1]*b[2] - a[2]*b[1],
        a[2]*b[0] - a[0]*b[2],
        a[0]*b[1] - a[1]*b[0]
    )



def vec_dot(a, b):
    return a[0]*b[0] + a[1]*b[1] + a[2]*b[2]



def vec_normalize(v):
    length = math.sqrt(vec_dot(v, v))
    if length == 0:
        return (0,0,0)
    return (v[0]/length, v[1]/length, v[2]/length)



def rotate_y(p, angle):
    x,y,z = p
    c = math.cos(angle)
    s = math.sin(angle)
    return (x*c + z*s, y, -x*s + z*c)



def rotate_x(p, angle):
    x,y,z = p
    c = math.cos(angle)
    s = math.sin(angle)
    return (x, y*c - z*s, y*s + z*c)





def project(p, width, height, fov):
    x,y,z = p
    if z == 0:
        z = 0.0001
    factor = fov / z
    sx = int(x * factor + width/2)
    sy = int(-y * factor + height/2)
    return (sx, sy, z)

# cube definition




cube_vertices = [
    (-1, -1, -1),
    ( 1, -1, -1),
    ( 1,  1, -1),
    (-1,  1, -1),
    (-1, -1,  1),
    ( 1, -1,  1),
    ( 1,  1,  1),
    (-1,  1,  1),
]




# 12 triangles (2 per face)
cube_triangles = [
    # Front
    (0,1,2), (0,2,3),
    # Back
    (5,4,7), (5,7,6),
    # Left
    (4,0,3), (4,3,7),
    # Right
    (1,5,6), (1,6,2),
    # Top
    (3,2,6), (3,6,7),
    # Bottom
    (4,5,1), (4,1,0)
]

light_dir = vec_normalize((0,0,-1))
shade_chars = " .:-=+*#%@"









# rasterizer

def draw_triangle(stdscr, pts, intensity, zbuffer):
    h = len(zbuffer)
    w = len(zbuffer[0])

    (x1,y1,z1), (x2,y2,z2), (x3,y3,z3) = pts

    min_x = max(min(x1,x2,x3), 0)
    max_x = min(max(x1,x2,x3), w-1)
    min_y = max(min(y1,y2,y3), 0)
    max_y = min(max(y1,y2,y3), h-1)

    def edge(x0,y0,x1,y1,x,y):
        return (x-x0)*(y1-y0) - (y-y0)*(x1-x0)

    area = edge(x1,y1,x2,y2,x3,y3)
    if area == 0:
        return

    char = shade_chars[int(intensity*(len(shade_chars)-1))]

    for y in range(min_y, max_y+1):
        for x in range(min_x, max_x+1):
            w0 = edge(x2,y2,x3,y3,x,y)
            w1 = edge(x3,y3,x1,y1,x,y)
            w2 = edge(x1,y1,x2,y2,x,y)

            if (w0 >= 0 and w1 >= 0 and w2 >= 0) or \
               (w0 <= 0 and w1 <= 0 and w2 <= 0):

                depth = (z1 + z2 + z3) / 3

                if depth < zbuffer[y][x]:
                    zbuffer[y][x] = depth
                    try:
                        stdscr.addch(y, x, char)
                    except:
                        pass

# main loop
def main(stdscr):
    curses.curs_set(0)
    stdscr.nodelay(True)
    stdscr.timeout(0)

    angle = 0
    fov = 60

    while True:
        height, width = stdscr.getmaxyx()
        stdscr.clear()
        zbuffer = [[float("inf") for _ in range(width)] for _ in range(height)]

        # Rotate and move cube
        rotated_vertices = []
        for v in cube_vertices:
            r = rotate_y(v, angle)
            r = rotate_x(r, angle*0.5)
            rotated_vertices.append((r[0], r[1], r[2]+5))

        # Draw all triangles
        for tri in cube_triangles:
            v0 = rotated_vertices[tri[0]]
            v1 = rotated_vertices[tri[1]]
            v2 = rotated_vertices[tri[2]]

            # Normal
            line1 = vec_sub(v1, v0)
            line2 = vec_sub(v2, v0)
            normal = vec_normalize(vec_cross(line1, line2))

            # Backface culling
            if vec_dot(normal, (0,0,-1)) < 0:
                intensity = max(0, vec_dot(normal, light_dir))
                projected = [project(v, width, height, fov) for v in [v0,v1,v2]]
                draw_triangle(stdscr, projected, intensity, zbuffer)

        stdscr.refresh()
        angle += 0.03
        time.sleep(0.016)

        if stdscr.getch() == 27:
            break


# infinite loop
curses.wrapper(main)