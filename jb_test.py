import sys
import os
import pygame
import time
from pygame.locals import *
from math import *

####------Colours------####
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
BROWN = (139, 69, 19)
CYAN = (0, 255, 255)
DARKBLUE = (0, 0, 64)
DARKBROWN = (36, 18, 5)
DARKGREEN = (0, 64, 0)
DARKGREY = (64, 64, 64)
DARKRED = (64, 0, 0)
GREY = (128, 128, 128)
GREEN = (0, 128, 0)
LIME = (0, 255, 0)
MAGENTA = (255, 0, 255)
MAROON = (128, 0, 0)
NAVYBLUE = (0, 0, 128)
OLIVE = (128, 128, 0)
PURPLE = (128, 0, 128)
RED = (255, 0, 0)
SILVER = (192, 192, 192)
TEAL = (0, 128, 128)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
####-------------------####

pygame.init()

path = os.path.join(os.path.split(__file__)[0], "data")

HEIGHT = WIDTH = 600

CLOCK = pygame.time.Clock()
FPS = 60
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.event.set_grab(True)

pygame.display.set_caption("Raycaster")
pygame.mouse.set_visible(False)

map_colour = MAROON
floor_colour = DARKBROWN
ceiling_colour = CYAN

rotate_speed = 0.01
move_speed = 0.075
strafe_speed = 0.04
wall_height = 1.27
resolution = 1  # Pixels per line

texture1 = pygame.image.load(os.path.join(path, "doors/Closed.png"))
texture2 = pygame.image.load(os.path.join(path, "test2.png"))
texture3 = pygame.image.load(os.path.join(path, "walls/MossyWall.png"))
texture4 = pygame.image.load(os.path.join(path, "walls/BloodWall.png"))
texWidth1, texHeight1 = texture1.get_width(), texture1.get_height()
texWidth2, texHeight2 = texture2.get_width(), texture2.get_height()
texWidth3, texHeight3 = texture3.get_width(), texture3.get_height()
texWidth4, texHeight4 = texture4.get_width(), texture4.get_height()
texArray1 = pygame.PixelArray(texture1)
texArray2 = pygame.PixelArray(texture2)
texArray3 = pygame.PixelArray(texture3)
texArray4 = pygame.PixelArray(texture4)
old = 0


def create_level(file):
    with open("data/Level.txt", "r", encoding="utf-8") as world_text:
        game_world = [list(map(int, a.split())) for a in world_text.read().split("\n")]
    return len(game_world[0]), len(game_world), game_world


def Quit():
    pygame.quit()
    sys.exit()


def layer_trace(
    x,
    sideDistX,
    sideDistY,
    deltaDistX,
    deltaDistY,
    mapBoundX,
    mapBoundY,
    side,
    mapX,
    mapY,
    rayPosX,
    rayPosY,
    stepX,
    stepY,
    rayDirX,
    rayDirY,
    mapGrid,
):
    # we need to go to the furthest point, and work back towards the ray origin
    # sort of works, you can see the further wall, but not yet added 'door' back as last item
    while True:
        # Jump to next map square
        if sideDistX < sideDistY:
            sideDistX += deltaDistX
            mapX += stepX
            side = 0
        else:
            sideDistY += deltaDistY
            mapY += stepY
            side = 1

        # Check if ray hits wall or leaves the map boundries
        if (
            mapX >= mapBoundX
            or mapY >= mapBoundY
            or mapX < 0
            or mapY < 0
            or mapGrid[mapX][mapY] != 0
        ):
            if mapGrid[mapX][mapY] != 2:
                break
    trace_column, yStart = raytrace(
        side, mapX, mapY, rayPosX, rayPosY, stepX, stepY, rayDirX, rayDirY, mapGrid
    )
    SCREEN.blit(trace_column, (x, yStart))
    return sideDistX, sideDistY, mapX, mapY


def raytrace(
    side, mapX, mapY, rayPosX, rayPosY, stepX, stepY, rayDirX, rayDirY, mapGrid
):
    # moved here so we can reuse the code
    # Calculate the total length of the ray
    if side == 0:
        rayLength = (mapX - rayPosX + (1 - stepX) / 2) / rayDirX
    else:
        rayLength = (mapY - rayPosY + (1 - stepY) / 2) / rayDirY

    # Calculate the length of the line to draw on the screen
    lineHeight = (HEIGHT / rayLength) * wall_height

    # Calculate the start and end point of each line
    drawStart = -lineHeight / 2 + (HEIGHT) / 2
    drawEnd = lineHeight / 2 + (HEIGHT) / 2

    # Calculate where exactly the wall was hit
    if side == 0:
        wallX = rayPosY + rayLength * rayDirY
    else:
        wallX = rayPosX + rayLength * rayDirX
    wallX = abs((wallX - floor(wallX)) - 1)

    # Find the x coordinate on the texture
    texX = int(wallX * eval("texWidth" + str(mapGrid[mapX][mapY])))
    if side == 0 and rayDirX > 0:
        texX = eval("texWidth" + str(mapGrid[mapX][mapY])) - texX - 1
    if side == 1 and rayDirY < 0:
        texX = eval("texWidth" + str(mapGrid[mapX][mapY])) - texX - 1

    c = max(1, (255.0 - rayLength * 27.2) * (1 - side * 0.25))

    yStart = max(0, drawStart)
    yStop = min(HEIGHT, drawEnd)
    pixelsPerTexel = lineHeight / eval("texHeight" + str(mapGrid[mapX][mapY]))
    colStart = int((yStart - drawStart) / pixelsPerTexel + 0.5)
    colHeight = int((yStop - yStart) / pixelsPerTexel + 0.5)

    yStart = int(colStart * pixelsPerTexel + drawStart + 0.5)
    yHeight = int(colHeight * pixelsPerTexel + 0.5)

    column = eval("texture" + str(mapGrid[mapX][mapY])).subsurface(
        (texX, colStart, 1, colHeight)
    )
    column = column.copy()
    column.fill((c, c, c), special_flags=BLEND_MULT)
    column = pygame.transform.scale(column, (resolution, yHeight))
    return column, yStart


def main():
    mapBoundX, mapBoundY, mapGrid = create_level("Level")

    posX, posY = 8.5, 10.5
    dirX, dirY = 1.0, 0.0
    planeX, planeY = 0.0, 0.66

    while True:

        # Input handling
        for event in pygame.event.get():
            if event.type == QUIT:
                Quit()
                return
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    Quit()
                    return

        # CEILING AND FLOOR
        pygame.draw.rect(SCREEN, ceiling_colour, (0, 0, WIDTH, (HEIGHT) / 2))
        pygame.draw.rect(SCREEN, floor_colour, (0, (HEIGHT) / 2, WIDTH, (HEIGHT) / 2))

        for x in range(0, WIDTH, resolution):
            # Initial setup
            cameraX = (2 * x / WIDTH - 1) / 2
            rayPosX, rayPosY = posX, posY
            # Add small value to avoid division by 0
            rayDirX = dirX + planeX * cameraX + 0.000000000000001
            # Add small value to avoid division by 0
            rayDirY = dirY + planeY * cameraX + 0.000000000000001

            # Which square on the map the ray is in
            mapX = int(rayPosX)
            mapY = int(rayPosY)

            # The length of one ray from one x-side or y-side to the next x-side or y-side
            deltaDistX = sqrt(1 + rayDirY**2 / rayDirX**2)
            deltaDistY = sqrt(1 + rayDirX**2 / rayDirY**2)

            # Calculate step and initial sideDist
            if rayDirX < 0:
                stepX = -1
                sideDistX = (rayPosX - mapX) * deltaDistX
            else:
                stepX = 1
                sideDistX = (mapX + 1 - rayPosX) * deltaDistX

            if rayDirY < 0:
                stepY = -1
                sideDistY = (rayPosY - mapY) * deltaDistY
            else:
                stepY = 1
                sideDistY = (mapY + 1 - rayPosY) * deltaDistY

            # Digital differential analysis (DDA)
            while True:
                # Jump to next map square
                if sideDistX < sideDistY:
                    sideDistX += deltaDistX
                    mapX += stepX
                    side = 0
                else:
                    sideDistY += deltaDistY
                    mapY += stepY
                    side = 1

                # Check if ray hits wall or leaves the map boundries
                if (
                    mapX >= mapBoundX
                    or mapY >= mapBoundY
                    or mapX < 0
                    or mapY < 0
                    or mapGrid[mapX][mapY] != 0
                ):
                    if mapGrid[mapX][mapY] != 2:
                        break
                    else:
                        # invoke layering
                        sideDistX, sideDistY, mapX, mapY = layer_trace(
                            x,
                            sideDistX,
                            sideDistY,
                            deltaDistX,
                            deltaDistY,
                            mapBoundX,
                            mapBoundY,
                            side,
                            mapX,
                            mapY,
                            rayPosX,
                            rayPosY,
                            stepX,
                            stepY,
                            rayDirX,
                            rayDirY,
                            mapGrid,
                        )
            # normal raytrace (closest thing is the only thing we can see)
            trace_column, yStart = raytrace(
                side,
                mapX,
                mapY,
                rayPosX,
                rayPosY,
                stepX,
                stepY,
                rayDirX,
                rayDirY,
                mapGrid,
            )
            SCREEN.blit(trace_column, (x, yStart))

        # Movement controls
        keys = pygame.key.get_pressed()

        if keys[K_w]:
            if not mapGrid[int(posX + dirX * move_speed)][int(posY)]:
                posX += dirX * move_speed
            if not mapGrid[int(posX)][int(posY + dirY * move_speed)]:
                posY += dirY * move_speed

        if keys[K_a]:
            if not mapGrid[int(posX + dirY * strafe_speed)][int(posY)]:
                posX += dirY * strafe_speed
            if not mapGrid[int(posX)][int(posY - dirX * strafe_speed)]:
                posY -= dirX * strafe_speed

        if keys[K_s]:
            if not mapGrid[int(posX - dirX * move_speed)][int(posY)]:
                posX -= dirX * move_speed
            if not mapGrid[int(posX)][int(posY - dirY * move_speed)]:
                posY -= dirY * move_speed

        if keys[K_d]:
            if not mapGrid[int(posX - dirY * strafe_speed)][int(posY)]:
                posX -= dirY * strafe_speed
            if not mapGrid[int(posX)][int(posY + dirX * strafe_speed)]:
                posY += dirX * strafe_speed

        # Look left and right
        # Mouse input
        difference = pygame.mouse.get_rel()[0]
        # Keyboard input
        if keys[K_q]:
            difference = -5
        if keys[K_e]:
            difference = 5

        # Vector rotation

        if difference != 0:
            cosrot = cos(difference * rotate_speed)
            sinrot = sin(difference * rotate_speed)
            old = dirX
            dirX = dirX * cosrot - dirY * sinrot
            dirY = old * sinrot + dirY * cosrot
            old = planeX
            planeX = planeX * cosrot - planeY * sinrot
            planeY = old * sinrot + planeY * cosrot

        pygame.display.update()
        CLOCK.tick(FPS)


if __name__ == "__main__":
    main()
