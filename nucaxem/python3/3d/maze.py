# made by someone else, fixed by me :)




import pygame
import math

pygame.init()

blick_genauigkeit = 0.02
laenge, hoehe = 800, 600

display = pygame.display.set_mode((laenge, hoehe))
pygame.display.set_caption("Catvasion")

ausfuehren = True
uhr = pygame.time.Clock()

weltenkarte = [
    [1,1,1,1,1,1,1,1,1,1,1,1],
    [1,0,1,0,0,1,0,0,0,1,0,1],
    [1,0,0,0,1,1,0,1,0,0,0,1],
    [1,0,0,0,0,0,0,0,0,1,0,1],
    [1,1,1,1,1,1,1,1,1,1,1,1]
]

sicht = 70
x_position, y_position = 1.5, 1.5
radiant = 0

bewegungs_schnelligkeit = 0.1
sensitivity = 0.05

lk = rk = uk = dk = schiessen = False

while ausfuehren:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            ausfuehren = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                lk = True
            elif event.key == pygame.K_RIGHT:
                rk = True
            elif event.key == pygame.K_UP:
                uk = True
            elif event.key == pygame.K_DOWN:
                dk = True
            elif event.key == pygame.K_SPACE:
                schiessen = True

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                lk = False
            elif event.key == pygame.K_RIGHT:
                rk = False
            elif event.key == pygame.K_UP:
                uk = False
            elif event.key == pygame.K_DOWN:
                dk = False
            elif event.key == pygame.K_SPACE:
                schiessen = False

    x, y = x_position, y_position

    if lk:
        x += bewegungs_schnelligkeit * math.cos(radiant)
        y += bewegungs_schnelligkeit * math.sin(radiant)

    if rk:
        x -= bewegungs_schnelligkeit * math.cos(radiant)
        y -= bewegungs_schnelligkeit * math.sin(radiant)

    if uk:
        radiant -= sensitivity

    if dk:
        radiant += sensitivity

    if weltenkarte[int(y)][int(x)] == 0:
        x_position, y_position = x, y

    display.fill((0, 0, 0))

    for sichtwert in range(sicht):
        radiant2 = radiant + math.radians(sichtwert - sicht / 2)

        x, y = x_position, y_position
        sin_a = blick_genauigkeit * math.sin(radiant2)
        cos_a = blick_genauigkeit * math.cos(radiant2)

        dist = 0

        while True:
            x += cos_a
            y += sin_a
            dist += 1

            if weltenkarte[int(y)][int(x)] != 0:
                break

        hoehe_linie = 600 / (dist * 0.02)
        farbe = 255 / (1 + dist * dist * 0.0001)

        pygame.draw.line(
            display,
            (farbe, farbe, farbe),
            (sichtwert * laenge / sicht, hoehe / 2 + hoehe_linie / 2),
            (sichtwert * laenge / sicht, hoehe / 2 - hoehe_linie / 2),
            int(laenge / sicht) + 1
        )

    pygame.display.flip()
    uhr.tick(60)

pygame.quit()
