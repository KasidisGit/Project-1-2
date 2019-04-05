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


class Ball:
    def __init__(self, position_x, position_y, radius, color):
        # Take the parameters of the init function above, and create instance variables out of them.
        self.position_x = position_x
        self.position_y = position_y
        self.radius = radius
        self.color = color

    def draw(self):
        """ Draw the balls with the instance variables we have. """
        arcade.draw_circle_filled(self.position_x, self.position_y, self.radius, self.color)


class Worm:
    def __init__(self, world, x, y):
        self.world = world
        self.x = self.world.boat.x
        self.y = self.world.boat.y
        self.vy = 5
        self.space = False
        self.score = 0

    def update(self, delta):
        self.move_down()
        if self.space:
            if self.world.fish1.x - 100 <= self.x <= self.world.fish1.x + 100 and self.world.fish1.y - 75 <= self.y <= self.world.fish1.y + 75:
                self.world.fish1.is_caught = True
                self.space = False
                self.move_up()

    def move_up(self):
        if self.space and not self.world.fish1.is_caught and self.space:
            self.y += self.vy

    def move_down(self):
        if self.space:
            self.y -= self.vy

    def back(self):
        self.x = self.world.boat.x
        self.y = self.world.boat.y


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

    def catch(self):
        if self.is_caught:
            self.vx = 0
            self.world.worm.y += self.vy
            self.y += self.vy
            if self.y >= self.world.boat.y - 55:
                self.stat = False
                self.back()

    def back(self):
        self.stat = True
        self.x = -200
        self.y = 40
        self.vx = 2
        arcade.draw_circle_filled(self.world.worm.x + 73, self.world.worm.y - 55, 1.3, arcade.color.BLACK)


class Fish3:
    def __init__(self, world, x, y):
        self.world = world
        self.x = x
        self.y = y
        self.is_caught = False

    def update(self):
        if not self.is_caught:
            self.x -= 2


class Fish4:
    def __init__(self, world, x, y):
        self.world = world
        self.x = x
        self.y = y
        self.is_caught = False

    def update(self):
        if not self.is_caught:
            self.x += 10


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
        self.fish1 = Fish1(self, -150, random.randint(20, 500))
        self.fish3 = Fish3(self, 1550, random.randint(20, 500))
        self.fish4 = Fish4(self, -150, random.randint(20, 500))
        self.state = World.STATE_FROZEN
        self.next_direction = DIR_STILL

    def update(self, delta):
        if self.state in [World.STATE_FROZEN, World.STATE_DEAD]:
            return
        self.boat.update(delta)
        self.worm.update(delta)
        self.fish1.update()
        self.fish1.catch()
        self.fish3.update()
        self.fish4.update()

    def start(self):
        self.state = World.STATE_STARTED

    def is_started(self):
        return self.state == World.STATE_STARTED

    def on_key_press(self, key, key_modifiers):
        if key in KEY_MAP:
            self.boat.next_direction = KEY_MAP[key]
        if key == arcade.key.SPACE:
            self.worm.space = True
