import arcade.key

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
    def __init__(self, world, x, y):
        self.world = world
        self.x = x
        self.y = y
        self.direction = DIR_STILL
        self.next_direction = DIR_STILL
        self.score = 0

    def move(self, direction):
        self.x += MOVEMENT_SPEED * DIR_OFFSETS[direction][0]
        self.y += MOVEMENT_SPEED * DIR_OFFSETS[direction][1]

    def update(self, delta):
        pass


class World:
    STATE_FROZEN = 1
    STATE_STARTED = 2
    STATE_DEAD = 3

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.boat = Boat(self, 700, 600)
        self.worm = Worm(self, 60, 100)
        self.state = World.STATE_FROZEN
        self.next_direction = DIR_STILL

    def update(self, delta):
        if self.state in [World.STATE_FROZEN,World.STATE_DEAD]:
            return
        self.boat.update(delta)

    def start(self):
        self.state = World.STATE_STARTED

    def is_started(self):
        return self.state == World.STATE_STARTED

    def on_key_press(self, key, key_modifiers):
        if key in KEY_MAP:
            self.boat.next_direction = KEY_MAP[key]
