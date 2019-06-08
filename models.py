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

increase_time = 30


class Background:
    def __init__(self, world, x, y):
        self.world = world
        self.x = x
        self.y = y


class Boat:
    def __init__(self, world, x, y):
        self.world = world
        self.direction = DIR_RIGHT
        self.next_direction = DIR_RIGHT
        self.x = x
        self.y = y
        self.boat_head = "R"

    def update(self, delta):
        if self.world.worm.space is not True:
            self.move(self.next_direction)

    def move(self, direction):
        if self.x >= -150:
            self.x += MOVEMENT_SPEED * DIR_OFFSETS[direction][0]
            if self.x >= 1550:
                self.x = 0
        else:
            self.x = 1400


class Worm:
    WORM_SPEED = 10

    def __init__(self, world, x, y):
        self.world = world
        self.x = self.world.boat.x
        self.y = self.world.boat.y
        self.space = False
        self.stat = True
        self.vy = 0
        self.score = 0
        self.is_hooked = False

    def update(self, delta):
        if self.is_hooked is False:
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

    def hooking(self):
        if self.space is False:
            self.is_hooked = True
            self.world.boat.direction = DIR_STILL
            self.vy = - Worm.WORM_SPEED
            self.space = True

    def back(self):
        self.vy = Worm.WORM_SPEED

    def move_up(self):
        if self.y < 600:
            self.y += self.vy
        else:
            self.y = 600
            self.vy = 0
            self.space = False
            self.stat = True
            self.is_hooked = False

    def move_down(self):
        self.y += self.vy


class Bone2:
    def __init__(self, world, x, y):
        self.world = world
        self.x = x
        self.y = y
        self.vx = 7
        self.vy = 7
        self.stat = True
        self.is_caught = False

    def update(self):
        if self.stat and self.x < 1400:
            self.x += self.vx
        else:
            self.back()

    def hit(self):
        if self.x - 170 <= self.world.worm.x <= self.x and self.y <= self.world.worm.y <= self.y + 50 \
                and self.world.boat.boat_head == "R":
            self.is_caught = True
            self.world.worm.stat = False
        if self.x + 47 <= self.world.worm.x <= self.x + 180 and self.y <= self.world.worm.y <= self.y + 50 \
                and self.world.boat.boat_head == "L":
            self.is_caught = True
            self.world.worm.stat = False

    def catch(self):
        if self.is_caught:
            self.vx = 0
            self.y += self.world.worm.vy
            if self.y >= self.world.boat.y - 70:
                self.world.time -= 20
                self.stat = False

    def back(self):
        self.x = -600
        self.y = random.randint(200, 500)
        self.vx = 7
        self.stat = True
        self.is_caught = False


class Bone:
    def __init__(self, world, x, y):
        self.world = world
        self.x = x
        self.y = y
        self.vx = 7
        self.vy = 7
        self.stat = True
        self.is_caught = False

    def update(self):
        if self.stat and self.x > 0:
            self.x -= self.vx
        else:
            self.back()

    def hit(self):
        if self.x - 200 <= self.world.worm.x <= self.x - 50 and self.y <= self.world.worm.y <= self.y + 50 \
                and self.world.boat.boat_head == "R":
            self.is_caught = True
            self.world.worm.stat = False
        if self.x - 40 <= self.world.worm.x <= self.x + 150 and self.y <= self.world.worm.y <= self.y + 50 \
                and self.world.boat.boat_head == "L":
            self.is_caught = True
            self.world.worm.stat = False

    def catch(self):
        if self.is_caught:
            self.vx = 0
            self.y += self.world.worm.vy
            if self.y >= self.world.boat.y - 70:
                self.world.time -= 20
                self.stat = False

    def back(self):
        self.x = 2000
        self.y = random.randint(200, 500)
        self.vx = 7
        self.stat = True
        self.is_caught = False


class Fish1:
    def __init__(self, world, x, y):
        self.world = world
        self.x = x
        self.y = y
        self.vx = 5
        self.vy = 7
        self.stat = True
        self.is_caught = False
        self.score = 300

    def update(self):
        if self.stat and self.x < 1400:
            self.x += self.vx
        else:
            self.back()

    def hit(self):
        if self.x - 50 <= self.world.worm.x <= self.x + 10 and self.y <= self.world.worm.y <= self.y + 50 \
                and self.world.boat.boat_head == "R":
            self.is_caught = True
            self.world.worm.stat = False
        if self.x <= self.world.worm.x <= self.x + 162 and self.y <= self.world.worm.y <= self.y + 50 \
                and self.world.boat.boat_head == "L":
            self.is_caught = True
            self.world.worm.stat = False

    def catch(self):
        if self.is_caught:
            self.vx = 0
            self.y += self.world.worm.vy
            if self.y >= self.world.boat.y - 70:
                self.world.all_score += self.score
                self.world.time += increase_time
                self.stat = False

    def back(self):
        self.x = -300
        self.y = random.randint(200, 500)
        self.vx = 5
        self.stat = True
        self.is_caught = False


class Fish2:
    def __init__(self, world, x, y):
        self.world = world
        self.x = x
        self.y = y
        self.vx = 6
        self.vy = 7
        self.stat = True
        self.is_caught = False
        self.score = 100

    def update(self):
        if self.stat and self.x < 1400:
            self.x += self.vx
        else:
            self.back()

    def hit(self):
        if self.x - 60 <= self.world.worm.x <= self.x + 10 and self.y <= self.world.worm.y <= self.y + 50 \
                and self.world.boat.boat_head == "R":
            self.is_caught = True
            self.world.worm.stat = False
        if self.x + 73 <= self.world.worm.x <= self.x + 123 and self.y <= self.world.worm.y <= self.y + 50 \
                and self.world.boat.boat_head == "L":
            self.is_caught = True
            self.world.worm.stat = False

    def catch(self):
        if self.is_caught:
            self.vx = 0
            self.y += self.world.worm.vy
            if self.y >= self.world.boat.y - 70:
                self.world.all_score += self.score
                self.world.time += increase_time
                self.stat = False

    def back(self):
        self.x = -500
        self.y = random.randint(200, 500)
        self.vx = 6
        self.stat = True
        self.is_caught = False


class Fish3:
    def __init__(self, world, x, y):
        self.world = world
        self.x = x
        self.y = y
        self.vx = 14
        self.vy = 7
        self.stat = True
        self.is_caught = False
        self.score = 1000

    def update(self):
        if self.stat and self.x < 1400:
            self.x += self.vx
        else:
            self.back()

    def hit(self):
        if self.x - 75 <= self.world.worm.x <= self.x + 10 and self.y - 10 <= self.world.worm.y <= self.y + 50 \
                and self.world.boat.boat_head == "R":
            self.is_caught = True
            self.world.worm.stat = False
        if self.x + 53 <= self.world.worm.x <= self.x + 162 and self.y - 10 <= self.world.worm.y <= self.y + 50 \
                and self.world.boat.boat_head == "L":
            self.is_caught = True
            self.world.worm.stat = False

    def catch(self):
        if self.is_caught:
            self.vx = 0
            self.y += self.world.worm.vy
            if self.y >= self.world.boat.y - 70:
                self.world.all_score += self.score
                self.world.time += increase_time
                self.stat = False

    def back(self):
        self.x = -2500
        self.y = random.randint(200, 300)
        self.vx = 14
        self.stat = True
        self.is_caught = False


class Fish4:
    def __init__(self, world, x, y):
        self.world = world
        self.x = x
        self.y = y
        self.vx = 5
        self.vy = 7
        self.stat = True
        self.is_caught = False
        self.score = 400

    def update(self):
        if self.stat and self.x > 0:
            self.x -= self.vx
        else:
            self.back()

    def hit(self):
        if self.x - 150 <= self.world.worm.x <= self.x - 75 and self.y <= self.world.worm.y <= self.y + 50 \
                and self.world.boat.boat_head == "R":
            self.is_caught = True
            self.world.worm.stat = False
        if self.x - 33 <= self.world.worm.x <= self.x + 123 and self.y <= self.world.worm.y <= self.y + 50 \
                and self.world.boat.boat_head == "L":
            self.is_caught = True
            self.world.worm.stat = False

    def catch(self):
        if self.is_caught:
            self.vx = 0
            self.y += self.world.worm.vy
            if self.y >= self.world.boat.y - 70:
                self.world.all_score += self.score
                self.world.time += increase_time
                self.stat = False

    def back(self):
        self.x = 1600
        self.y = random.randint(200, 500)
        self.vx = 5
        self.stat = True
        self.is_caught = False


class Fish5:
    def __init__(self, world, x, y):
        self.world = world
        self.x = x
        self.y = y
        self.vx = 6
        self.vy = 7
        self.stat = True
        self.is_caught = False
        self.score = 200

    def update(self):
        if self.stat and self.x > 0:
            self.x -= self.vx
        else:
            self.back()

    def hit(self):
        if self.x - 150 <= self.world.worm.x <= self.x - 75 and self.y <= self.world.worm.y <= self.y + 50 \
                and self.world.boat.boat_head == "R":
            self.is_caught = True
            self.world.worm.stat = False
        if self.x - 25 <= self.world.worm.x <= self.x + 123 and self.y <= self.world.worm.y <= self.y + 50 \
                and self.world.boat.boat_head == "L":
            self.is_caught = True
            self.world.worm.stat = False

    def catch(self):
        if self.is_caught:
            self.vx = 0
            self.y += self.world.worm.vy
            if self.y >= self.world.boat.y - 70:
                self.world.all_score += self.score
                self.world.time += increase_time
                self.stat = False

    def back(self):
        self.x = 2000
        self.y = random.randint(200, 500)
        self.vx = 6
        self.stat = True
        self.is_caught = False


class World:
    STATE_FROZEN = 1
    STATE_STARTED = 2
    STATE_DEAD = 3

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.background_1 = Background(self, 700, 400)
        self.background_2 = Background(self, 700, 400)
        self.background_3 = Background(self, 700, 400)
        self.background_4 = Background(self, 700, 400)
        self.boat = Boat(self, 700, 600)
        self.worm = Worm(self, 700, 600)
        self.time = 1300
        self.all_score = 0
        self.bone = Bone(self, 1900, random.randint(200, 500))
        self.bone2 = Bone2(self, -500, random.randint(200, 500))
        self.fish1 = Fish1(self, -300, random.randint(200, 500))
        self.fish2 = Fish2(self, -700, random.randint(200, 500))
        self.fish3 = Fish3(self, -3000, random.randint(200, 300))
        self.fish4 = Fish4(self, 2000, random.randint(200, 500))
        self.fish5 = Fish5(self, 2500, random.randint(200, 500))
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
        self.fish2.update()
        self.fish2.hit()
        self.fish2.catch()
        self.fish3.update()
        self.fish3.hit()
        self.fish3.catch()
        self.fish4.update()
        self.fish4.hit()
        self.fish4.catch()
        self.fish5.update()
        self.fish5.hit()
        self.fish5.catch()
        self.bone.update()
        self.bone.hit()
        self.bone.catch()
        self.bone2.update()
        self.bone2.hit()
        self.bone2.catch()

    def start(self):
        self.state = World.STATE_STARTED

    def is_started(self):
        return self.state == World.STATE_STARTED

    def died(self):
        self.state = World.STATE_DEAD

    def reset(self):
        self.time = 1300
        self.all_score = 0
        self.next_direction = DIR_STILL
        self.fish1.back()
        self.fish2.back()
        self.fish3.back()
        self.fish4.back()
        self.fish5.back()
        self.bone.back()
        self.bone2.back()

    def on_key_press(self, key, key_modifiers):
        if key in KEY_MAP:
            if self.worm.space is False:
                self.boat.next_direction = KEY_MAP[key]
                if key == arcade.key.RIGHT:
                    self.boat.boat_head = "R"
                elif key == arcade.key.LEFT:
                    self.boat.boat_head = "L"
        if key == arcade.key.SPACE:
            self.worm.hooking()
