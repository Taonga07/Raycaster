from pygame import init, QUIT, K_UP, K_DOWN, K_LEFT, K_RIGHT
from math import pi, radians, sin, cos
from pygame.display import set_mode
from pygame.key import get_pressed
from pygame.display import update
from pygame.time import Clock
from pygame.draw import line
from pygame.event import get


init()  # pylint: disable=E1101
SCREEEN_SIZE, VIEWSIZE = 300, 60
window = set_mode((SCREEEN_SIZE, SCREEEN_SIZE))
clock = Clock()
GameWorld = [a.split() for a in open("GameWorlds/World.txt").read().split("\n")]
playerposx, playerposy, look_dir, player_speed = 2, 1, 30, 0.01


def fancy_maths():
    rot_i = (pi / 4) + radians(i - look_dir)
    x, y, n = playerposx, playerposy, 0
    tsin, tcos = 0.02 * sin(rot_i), 0.02 * cos(rot_i)
    while True:
        x, y, n = x + tcos, y + tsin, n + 1
        if GameWorld[int(x)][int(y)] != "0":
            height = (1 / (0.02 * n)) * SCREEEN_SIZE
            return height


def move_player(move_dir, posx, posy):
    look_rad = radians(look_dir)
    posy += move_dir * player_speed * cos(look_rad)
    posx += move_dir * player_speed * sin(look_rad)
    return posx, posy


while True:
    window.fill((0, 0, 0))
    for event in get():
        if event.type == QUIT:
            exit()
    keys = get_pressed()
    if keys[K_UP]:
        playerposx, playerposy = move_player(1, playerposx, playerposy)
    if keys[K_DOWN]:
        playerposx, playerposy = move_player(-1, playerposx, playerposy)
    if keys[K_LEFT]:
        look_dir += 0.5
    if keys[K_RIGHT]:
        look_dir -= 0.5
    for i in range(VIEWSIZE):
        height = fancy_maths()
        linex = i + (i * (SCREEEN_SIZE / VIEWSIZE))
        line(
            window,
            (125, 125, 125),
            (linex, ((SCREEEN_SIZE / 2) + (height / 2))),
            (linex, ((SCREEEN_SIZE / 2) - (height / 2))),
        )
    update()
    clock.tick(60)
