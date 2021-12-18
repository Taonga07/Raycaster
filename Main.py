from pygame import init, QUIT, K_UP, K_DOWN, K_w, K_s, KEYDOWN, K_ESCAPE
from pygame.mouse import get_rel, set_visible
from pygame.event import get, set_grab
from math import pi, radians, sin, cos
from pygame.display import set_mode
from pygame.key import get_pressed
from pygame.display import update
from pygame.time import Clock
from pygame.draw import polygon


class GameObject:
    """Main Game Code"""

    def __init__(self, game_world) -> None:
        self.SCREEN_SIZE, self.CAMERA_VIEWSIZE = 600, 60  # pylint: disable=invalid-name
        self.screen = set_mode((self.SCREEN_SIZE, self.SCREEN_SIZE))
        self.running, self.world, self.clock = True, game_world, Clock()
        _, camera_pos = (set_visible(False), set_grab(True)), self.get_camera_pos()
        self.camera = Camera(camera_pos, self.CAMERA_VIEWSIZE)

    def get_camera_pos(self):
        """set starting pos of camera"""
        if "2" in self.world:
            for x in range(len(self.world)):
                for y in range(len(self.world[x])):
                    if self.world[x][y] == "2":
                        return [x, y]
        self.world[1][1] = "2"
        return [1, 1]

    def main_game_loop(self):
        """will get events and call functions from them"""
        while self.running:
            self.screen.fill((0, 0, 0))
            self.check_for_user_event()
            self.check_for_quit()
            self.show_camera_view()
            update()
            self.clock.tick(60)
        exit()

    def show_camera_view(self):
        """draw veiw recived by camera"""
        self.camera.get_view(self.world, self.SCREEN_SIZE, self.screen)

    def check_for_quit(self):
        """check for esc key pressed and close window"""
        for event in get():
            if event.type == QUIT:
                self.running = False
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    self.running = False

    def check_for_user_event(self):
        """check for user events and respond"""
        keys = get_pressed()
        if keys[K_UP] or keys[K_w]:
            self.camera.move(1)
        if keys[K_DOWN] or keys[K_s]:
            self.camera.move(-1)
        self.camera.direction -= get_rel()[0]


class Camera:
    """class like a player but you see through its eyes"""

    def __init__(self, pos, viewsize) -> None:
        self.viewsize, self.pos, self.direction, self.speed = viewsize, pos, 30, 0.01

    def get_view(self, world, SCREEN_SIZE, screen):  # pylint: disable=invalid-name
        """use raycasting technic to generate 3D image"""
        for i in range(self.viewsize):
            if i == 0:
                old_height, old_pos = self.look_at_angle(i, world, SCREEN_SIZE)
                old_linex = i + (i * (SCREEN_SIZE / self.viewsize))
            else:
                height, pos = self.look_at_angle(i, world, SCREEN_SIZE)
                if pos != old_pos:
                    continue
                else:
                    linex = i + (i * (SCREEN_SIZE / self.viewsize))
                    polygon(
                        screen,
                        (125, 125, 125),
                        [
                            (linex, ((SCREEN_SIZE / 2) + (height / 2))),
                            (linex, ((SCREEN_SIZE / 2) - (height / 2))),
                            (old_linex, ((SCREEN_SIZE / 2) + (old_height / 2))),
                            (old_linex, ((SCREEN_SIZE / 2) - (old_height / 2))),
                        ],
                    )

    def look_at_angle(self, i, world, SCREEN_SIZE):  # pylint: disable=invalid-name
        """get height of one part of the image you are looking at"""
        rot_i = (pi / 4) + radians(i - self.direction)
        x, y, n = self.pos[0], self.pos[1], 0
        tsin, tcos = 0.02 * sin(rot_i), 0.02 * cos(rot_i)
        while True:
            x, y, n = x + tcos, y + tsin, n + 1
            if world[int(x)][int(y)] == "1":
                height = (1 / (0.02 * n)) * SCREEN_SIZE
                return height, (int(x), int(y))

    def move(self, move_dir):
        """move camera in direction backwards or forwards"""
        look_rad = radians(self.direction)
        self.pos[1] += move_dir * self.speed * cos(look_rad)
        self.pos[0] += move_dir * self.speed * sin(look_rad)


if __name__ == "__main__":
    init()  # pylint: disable=E1101
    with open("World.txt", "r", encoding="utf-8") as world_text:
        game_world = [a.split() for a in world_text.read().split("\n")]
    my_game = GameObject(game_world)
    my_game.main_game_loop()
