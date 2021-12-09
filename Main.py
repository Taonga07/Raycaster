from math import pi, radians, sin, cos
from time import sleep
import pygame

pygame.init()  # pylint: disable=E1101
SCREEEN_SIZE, VIEWSIZE = 300, 60
window = pygame.display.set_mode((SCREEEN_SIZE, SCREEEN_SIZE))
clock = pygame.time.Clock()
GameWorld = [a.split() for a in open("GameWorlds/World.txt").read().split("\n")]
playerposx, playerposy = 2, 1

def fancy_maths():
    rot_i = (pi / 4) + radians(i - 30)
    x, y, n = playerposx, playerposy, 0
    tsin, tcos = 0.02 * sin(rot_i), 0.02 * cos(rot_i)
    while True:
        x, y, n = x + tcos, y + tsin, n + 1
        if GameWorld[int(x)][int(y)] != "0":
            height = (1 / (0.02 * n)) * SCREEEN_SIZE
            return height

while True:
    print(playerposx, playerposy)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_UP:
                playerposx += 1
            if event.key == pygame.K_DOWN:
                playerposx -= 1
            if event.key == pygame.K_LEFT:
                playerposy += 1
            if event.key == pygame.K_RIGHT:
                playerposy -= 1
    for i in range(VIEWSIZE):
        height = fancy_maths()
        linex = i+(i*(SCREEEN_SIZE/VIEWSIZE))
        pygame.draw.line(window,(125, 125, 125), (linex, ((SCREEEN_SIZE / 2) + (height / 2))), (linex,((SCREEEN_SIZE / 2) - (height / 2))))
    pygame.display.flip()
    clock.tick()
