import arcade
from mol_project import *

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

        arcade.set_background_color(arcade.color.SEA_BLUE)
        self.world = World(SCREEN_WIDTH, SCREEN_HEIGHT)
        self.boat_sprite_l = ModelSprite("boatL.png", model=self.world.boat)
        self.boat_sprite_r = ModelSprite("boatR.png", model=self.world.boat)
        self.fish_sprite = ModelSprite("fish1.png", model=self.world.fish)

    def update(self, delta):
        self.world.update(delta)

    def on_draw(self):
        arcade.start_render()
        if self.world.boat.next_direction == 2:
            self.boat_sprite_r.draw()
        elif self.world.boat.next_direction == 4:
            self.boat_sprite_l.draw()
        else:
            self.boat_sprite_r.draw()
        self.fish_sprite.draw()

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
