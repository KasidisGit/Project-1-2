import arcade
from models import *

SCREEN_WIDTH = 1400
SCREEN_HEIGHT = 800


class ModelSprite(arcade.Sprite):
    def __init__(self, *args, **kwargs):
        self.model = kwargs.pop('model', None)
        super().__init__(*args, **kwargs)

    def sync_with_model(self):
        if self.model:
            self.set_position(self.model.x, self.model.y)

    def draw(self):
        self.sync_with_model()
        super().draw()


class Window(arcade.Window):
    def __init__(self, width, height):
        super().__init__(width, height)

        self.world = World(SCREEN_WIDTH, SCREEN_HEIGHT)
        self.background = ModelSprite("BG2.jpg", model=self.world.background)
        self.boat_sprite_l = ModelSprite("boatL.png", model=self.world.boat)
        self.boat_sprite_r = ModelSprite("boatR.png", model=self.world.boat)
        self.fish_sprite_1 = ModelSprite("fish1.png", model=self.world.fish1)

    def update(self, delta):
        self.world.update(delta)

    def on_draw(self):
        arcade.start_render()
        self.background.draw()
        if self.world.worm.y >= 0:
            if self.world.boat.next_direction == 2:
                self.boat_sprite_r.draw()
                arcade.draw_circle_filled(self.world.worm.x + 73, self.world.worm.y - 55, 10, arcade.color.BLACK)
            elif self.world.boat.next_direction == 4:
                self.boat_sprite_l.draw()
                arcade.draw_circle_filled(self.world.worm.x - 73, self.world.worm.y - 55, 10, arcade.color.BLACK)
            else:
                self.boat_sprite_r.draw()
                arcade.draw_circle_filled(self.world.worm.x + 73, self.world.worm.y - 55, 10, arcade.color.BLACK)
        if self.world.fish1.stat:
            self.fish_sprite_1.draw()

    def on_key_press(self, key, key_modifiers):
        if not self.world.is_started():
            self.world.start()
        self.world.on_key_press(key, key_modifiers)


def main():
    window = Window(SCREEN_WIDTH, SCREEN_HEIGHT)
    arcade.set_window(window)
    arcade.run()


if __name__ == '__main__':
    main()

