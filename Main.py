from math import pi, radians, sin, cos 
from matplotlib import pyplot
# import pygame

GameWorld = [a.split() for a in open("GameWorlds/World.txt").read().split('\n')]
playerposx, playerposy = 2, 1

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
    pyplot.vlines(i, -height, height)
pyplot.show()