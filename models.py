import arcade.key
import random
import arcade

MOVEMENT_SPEED = 4
DIR_STILL = 0
DIR_UP = 1
DIR_RIGHT = 2
DIR_DOWN = 3
DIR_LEFT = 4

DIR_OFFSETS = {DIR_STILL: (0, 0),
               DIR_UP: (0, 1),
               DIR_RIGHT: (1, 0),
               DIR_DOWN: (0, -1),
               DIR_LEFT: (-1, 0)}

KEY_MAP = {arcade.key.UP: DIR_UP,
           arcade.key.DOWN: DIR_DOWN,
           arcade.key.LEFT: DIR_LEFT,
           arcade.key.RIGHT: DIR_RIGHT, }


class Background:
    def __init__(self, world, x, y):
        self.world = world
        self.x = x
        self.y = y


class Boat:
    def __init__(self, world, x, y):
        self.world = world
        self.direction = DIR_STILL
        self.next_direction = DIR_STILL
        self.x = x
        self.y = y

    def update(self, delta):
        self.move(self.next_direction)

    def move(self, direction):
        self.x += MOVEMENT_SPEED * DIR_OFFSETS[direction][0]


class Worm:
    WORM_SPEED = 10

    def __init__(self, world, x, y):
        self.world = world
        self.x = self.world.boat.x
        self.y = self.world.boat.y
        self.stat = True
        self.vy = 0
        self.score = 0
        self.count = 1

    def update(self, delta):
        if self.count == 1:
            self.x = self.world.boat.x
            self.y = self.world.boat.y
        if self.stat:
            if self.y > 0 and self.vy <= 0:
                self.move_down()
            else:
                self.back()
                self.move_up()
        else:
            self.back()
            self.move_up()

    def attack(self):
        self.count = 0
        self.world.boat.next_direction = DIR_STILL
        self.vy = - Worm.WORM_SPEED

    def back(self):
        self.vy = Worm.WORM_SPEED

    def move_up(self):
        if self.y < 600:
            self.y += self.vy
        else:
            self.y = 600
            self.vy = 0
            self.stat = True
            self.count = 1

    def move_down(self):
        self.y += self.vy


class Fish1:
    def __init__(self, world, x, y):
        self.world = world
        self.x = x
        self.y = y
        self.vx = 5
        self.vy = 5
        self.stat = True
        self.is_caught = False

    def update(self):
        if self.stat:
            self.x += self.vx

    def hit(self):
        if self.x - 50 <= self.world.worm.x <= self.x + 50 and self.y - 75 <= self.world.worm.y <= self.y + 75:
            self.is_caught = True
            self.world.worm.stat = False

    def catch(self):
        if self.is_caught:
            self.vx = 0
            self.y += self.vy
            if self.y >= self.world.boat.y - 55:
                self.stat = False


class World:
    STATE_FROZEN = 1
    STATE_STARTED = 2
    STATE_DEAD = 3

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.background = Background(self, 700, 400)
        self.boat = Boat(self, 700, 600)
        self.worm = Worm(self, 700, 600)
        self.fish_list = []
        self.fish1 = Fish1(self, -150, random.randint(200, 500))
        self.state = World.STATE_FROZEN
        self.next_direction = DIR_STILL

    def update(self, delta):
        if self.state in [World.STATE_FROZEN, World.STATE_DEAD]:
            return
        self.boat.update(delta)
        self.worm.update(delta)
        self.fish1.update()
        self.fish1.hit()
        self.fish1.catch()

    def start(self):
        self.state = World.STATE_STARTED

    def is_started(self):
        return self.state == World.STATE_STARTED

    def on_key_press(self, key, key_modifiers):
        if key in KEY_MAP:
            self.boat.next_direction = KEY_MAP[key]
        if key == arcade.key.SPACE:
            self.worm.attack()
