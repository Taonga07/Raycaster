from pygame import init, QUIT, K_UP, K_DOWN, K_w, K_s, KEYDOWN, K_ESCAPE
from pygame.mouse import get_pos, set_visible
from math import pi, radians, sin, cos
from pygame.display import set_mode
from pygame.key import get_pressed
from pygame.display import update
from pygame.time import Clock
from pygame.draw import line
from pygame.event import get, set_grab
from sys import exit


class GameObject:
    def __init__(self, GameWorld) -> None:
        self.SCREEN_SIZE, self.CAMERA_VIEWSIZE = 300, 60
        self.screen = set_mode((self.SCREEN_SIZE, self.SCREEN_SIZE))
        set_visible(0)
        set_grab(1)
        self.running, self.World, self.clock = True, GameWorld, Clock()

    def CreateCamera(self):
        if "2" in self.World:
            for x in range(len(self.World)):
                for y in range(len(self.World[x])):
                    if self.World[x][y] == "2":
                        pos = [x, y]
        else:
            pos = [1, 1]
            self.World[1][1] = "2"
        self.camera = Camera(pos, self.CAMERA_VIEWSIZE)

    def MainGameLoop(self):
        while self.running:
            self.screen.fill((0, 0, 0))
            self.CheckForUserEvent()
            self.CheckForQuit()
            self.camera.GetView(self.World, self.SCREEN_SIZE, self.screen)
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
        if keys[K_UP] or keys[K_w]:
            self.camera.move(1)
        if keys[K_DOWN] or keys[K_s]:
            self.camera.move(-1)
        self.camera.change_dir(self.SCREEN_SIZE, get_pos())


class Camera:
    def __init__(self, pos, viewsize) -> None:
        self.viewsize, self.pos, self.direction, self.speed = viewsize, pos, 30, 0.01

    def GetView(self, World, SCREEN_SIZE, screen):
        for i in range(self.viewsize):
            height = self.LookAtAngle(i, World, SCREEN_SIZE)
            linex = i + (i * (SCREEN_SIZE / self.viewsize))
            line(
                screen,
                (125, 125, 125),
                (linex, ((SCREEN_SIZE / 2) + (height / 2))),
                (linex, ((SCREEN_SIZE / 2) - (height / 2))),
            )

    def LookAtAngle(self, i, World, SCREEN_SIZE):  # i = for angle in veiwsize
        rot_i = (pi / 4) + radians(i - self.direction)
        x, y, n = self.pos[0], self.pos[1], 0
        tsin, tcos = 0.02 * sin(rot_i), 0.02 * cos(rot_i)
        while True:
            x, y, n = x + tcos, y + tsin, n + 1
            if World[int(x)][int(y)] == "1":
                height = (1 / (0.02 * n)) * SCREEN_SIZE
                return height

    def move(self, move_dir):
        look_rad = radians(self.direction)
        self.pos[1] += move_dir * self.speed * cos(look_rad)
        self.pos[0] += move_dir * self.speed * sin(look_rad)

    def change_dir(self, SCREEN_SIZE, mouse_pos):
        self.direction = (SCREEN_SIZE / 2) + (mouse_pos[0] * -1)


if __name__ == "__main__":
    init()  # pylint: disable=E1101
    game_world = [a.split() for a in open("GameWorlds/World.txt").read().split("\n")]
    my_game = GameObject(game_world)
    my_game.CreateCamera()
    my_game.MainGameLoop()
