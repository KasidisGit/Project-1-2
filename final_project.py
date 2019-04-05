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

        # arcade.set_background_color(arcade.color.SEA_BLUE)
        self.world = World(SCREEN_WIDTH, SCREEN_HEIGHT)
        # self.set_mouse_visible(False)
        # self.ball = Ball(50, 50, 15, arcade.color.AUBURN)
        self.background = ModelSprite("BG2.jpg", model=self.world.background)
        self.boat_sprite_l = ModelSprite("boatL.png", model=self.world.boat)
        self.boat_sprite_r = ModelSprite("boatR.png", model=self.world.boat)
        self.fish_sprite_1 = ModelSprite("fish1.png", model=self.world.fish1)
        self.fish_sprite_3 = ModelSprite("fish3.png", model=self.world.fish3)
        self.fish_sprite_4 = ModelSprite("fish4.png", model=self.world.fish4)

    def update(self, delta):
        self.world.update(delta)

    def on_draw(self):
        arcade.start_render()
        self.background.draw()
        if self.world.boat.next_direction == 2:
            self.boat_sprite_r.draw()
        elif self.world.boat.next_direction == 4:
            self.boat_sprite_l.draw()
        else:
            self.boat_sprite_r.draw()
        if self.world.worm.space:
            if self.world.worm.y >= 0:
                arcade.draw_circle_filled(self.world.worm.x + 73, self.world.worm.y - 55, 1.3, arcade.color.BLACK)
        if self.world.fish1.stat:
            self.fish_sprite_1.draw()
        self.fish_sprite_3.draw()
        self.fish_sprite_4.draw()

    def on_key_press(self, key, key_modifiers):
        if not self.world.is_started():
            self.world.start()
        self.world.on_key_press(key, key_modifiers)

    # def on_mouse_motion(self, x, y, dx, dy):
    #     """ Called to update our objects. Happens approximately 60 times per second."""
    #     self.ball.position_x = x
    #     self.ball.position_y = y
    #
    # def on_mouse_press(self, x, y, button, modifiers):
    #     """
    #     Called when the user presses a mouse button.
    #     """
    #     print(f"You clicked button number: {button}")
    #     if button == arcade.MOUSE_BUTTON_LEFT:
    #         self.ball.color = arcade.color.BLACK
    #
    # def on_mouse_release(self, x, y, button, modifiers):
    #     """
    #     Called when a user releases a mouse button.
    #     """
    #     if button == arcade.MOUSE_BUTTON_LEFT:
    #         self.ball.color = arcade.color.AUBURN


def main():
    window = Window(SCREEN_WIDTH, SCREEN_HEIGHT)
    arcade.set_window(window)
    arcade.run()


if __name__ == '__main__':
    main()
