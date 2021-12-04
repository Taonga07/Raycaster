from math import pi, radians, sin, cos 
import pygame

pygame.init()
window = pygame.display.set_mode((300, 300))
GameWorld = [a.split() for a in open("GameWorlds/World.txt").read().split('\n')]
playerposx, playerposy = 2, 1

while True:
    for i in range(60):
        rot_i = (pi/4) + radians(i - 30)
        x, y, n = playerposx, playerposy, 0
        tsin, tcos = 0.02*sin(rot_i), 0.02*cos(rot_i)
        while True:
            x, y, n = x+tcos, y+tsin, n+1
            if GameWorld[int(x)][int(y)] != '0':
                height = 1/(0.02*n)
                print(height)
                break
        pygame.draw.line(window, (0, 0, 0), (i, -height), (i, height))
    pygame.display.update()