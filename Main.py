from pygame import init, QUIT, K_UP, K_DOWN, K_LEFT, K_RIGHT, KEYDOWN, K_ESCAPE
from math import pi, radians, sin, cos
from pygame.display import set_mode
from pygame.key import get_pressed
from pygame.display import update
from pygame.time import Clock
from pygame.draw import line
from pygame.event import get
from CONSTANTS import *
from sys import exit

class GameObject:
    def __init__(self, GameWorld) -> None:
            self.screen = set_mode((SCREEEN_SIZE, SCREEEN_SIZE))
            self.running, self.World, self.clock = True, GameWorld, Clock()
    def CreateCamera(self):
        for x in range(len(self.World)):
            for y in range(len(self.World[x])):
                if self.World[x][y] == "2":
                    pos = (x, y)
                else: 
                    pos = (1, 1)
                    self.World[x][y] = "2"
        self.camera = Camera(pos)
    def MainGameLoop(self):
        while self.running:
            self.screen.fill((0, 0, 0))
            self.CheckForUserEvent()
            self.CheckForQuit()
            self.camera.GetView(self.World)
            update()
            self.clock.tick(60)
        exit()
    def CheckForQuit(self):
        for event in get():
            if event.type == QUIT:
                self.running = False
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    self.running = False
    def CheckForUserEvent(self):
        keys = get_pressed()
        if keys[K_UP]:
            self.camera.move(1, self.camera.pos[0], self.camera.pos[1])
        if keys[K_DOWN]:
            self.camera.move(-1, self.camera.pos[0], self.camera.pos[1])
        if keys[K_LEFT]:
            self.camera.direction += 0.5
        if keys[K_RIGHT]:
            self.camera.direction -= 0.5
class Camera: 
    def __init__(self, pos) -> None:
        self.pos, self.direction, self.speed = pos, 30, 0.001
    def GetView(self, World):
        for i in range(CAMERA_VIEWSIZE):
            height = self.LookAtAngle(i, World)
            linex = i + (i * (SCREEEN_SIZE / CAMERA_VIEWSIZE))
            line(
                self.screen,
                (125, 125, 125),
                (linex, ((SCREEEN_SIZE / 2) + (height / 2))),
                (linex, ((SCREEEN_SIZE / 2) - (height / 2))),
            )
    def LookAtAngle(self, i, World): # i = for angle in veiwsize
        rot_i = (pi / 4) + radians(i - self.direction)
        x, y, n = self.pos[0], self.pos[1], 0
        tsin, tcos = 0.02 * sin(rot_i), 0.02 * cos(rot_i)
        while True:
            x, y, n = x + tcos, y + tsin, n + 1
            if World[int(x)][int(y)] != "0":
                height = (1 / (0.02 * n)) * self.SCREEEN_SIZE
                return height
    def move_player(self):
        look_rad = radians(self.direction)
        self.pos[0] += self.direction * self.speed * cos(look_rad)
        self.pos[1] += self.direction * self.speed * sin(look_rad)
if __name__ == "__main__":
    init()  # pylint: disable=E1101
    game_world = [a.split() for a in open("GameWorlds/World.txt").read().split("\n")]
    my_game = GameObject(game_world)
    my_game.CreateCamera()
    my_game.MainGameLoop()