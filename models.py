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
        self.background_1 = ModelSprite("BG2.jpg", model=self.world.background_1)
        self.background_2 = ModelSprite("BG2 Dark.jpg", model=self.world.background_2)
        self.background_3 = ModelSprite("start text.png", model=self.world.background_3)
        self.background_4 = ModelSprite("Gameover.png", model=self.world.background_4)
        self.boat_sprite_l = ModelSprite("boatL.png", model=self.world.boat)
        self.boat_sprite_r = ModelSprite("boatR.png", model=self.world.boat)
        self.fish_sprite_1 = ModelSprite("fish1.png", model=self.world.fish1)
        self.fish_sprite_2 = ModelSprite("fish7.png", model=self.world.fish2)
        self.fish_sprite_3 = ModelSprite("fish4.png", model=self.world.fish3)
        self.fish_sprite_4 = ModelSprite("fish5.png", model=self.world.fish4)
        self.fish_sprite_5 = ModelSprite("fish3.png", model=self.world.fish5)
        self.bone_sprite = ModelSprite("boney.png", model=self.world.bone)
        self.bone_sprite_r = ModelSprite("bone.png", model=self.world.bone2)

    def update(self, delta):
        if self.world.time > 900 and self.world.state == 2:
            self.world.time -= 0.5
        if self.world.time > 1300:
            self.world.time = 1300
        self.world.update(delta)

    def on_draw(self):
        arcade.start_render()

        if self.world.time <= 900:
            self.world.died()
            self.background_2.draw()
            self.background_4.draw()
            arcade.draw_text("High Score : " + str(self.world.all_score), SCREEN_WIDTH / 2, 150, arcade.color.BLACK, 35,
                             2000, align="center", anchor_x="center", anchor_y="center")

        if self.world.state == 2:
            self.background_1.draw()
            if self.world.worm.y >= 0:
                if self.world.boat.next_direction == 2:
                    self.boat_sprite_r.draw()
                    arcade.draw_circle_filled(self.world.worm.x + 73, self.world.worm.y - 55, 7, arcade.color.BLACK)
                elif self.world.boat.next_direction == 4:
                    self.boat_sprite_l.draw()
                    arcade.draw_circle_filled(self.world.worm.x - 73, self.world.worm.y - 55, 7, arcade.color.BLACK)
                else:
                    self.boat_sprite_r.draw()
                    arcade.draw_circle_filled(self.world.worm.x + 73, self.world.worm.y - 55, 7, arcade.color.BLACK)
            if self.world.fish1.stat:
                self.fish_sprite_1.draw()
            if self.world.fish2.stat:
                self.fish_sprite_2.draw()
            if self.world.fish3.stat:
                self.fish_sprite_3.draw()
            if self.world.fish4.stat:
                self.fish_sprite_4.draw()
            if self.world.fish5.stat:
                self.fish_sprite_5.draw()
            if self.world.bone.stat:
                self.bone_sprite.draw()
            if self.world.bone2.stat:
                self.bone_sprite_r.draw()

            arcade.draw_rectangle_outline(1100, 750.5, 400, 23.5, arcade.color.WHITE, border_width=5)
            arcade.draw_line(900, 757.5, self.world.time, 757.5, arcade.color.RED, border_width=10)
            arcade.draw_line(900, 755, self.world.time, 755, arcade.color.RED, border_width=10)
            arcade.draw_line(900, 752.5, self.world.time, 752.5, arcade.color.RED, border_width=10)
            arcade.draw_line(900, 750, self.world.time, 750, arcade.color.RED, border_width=10)
            arcade.draw_line(900, 747.5, self.world.time, 747.5, arcade.color.RED, border_width=10)
            arcade.draw_line(900, 745, self.world.time, 745, arcade.color.RED, border_width=10)
            arcade.draw_line(900, 742.5, self.world.time, 742.5, arcade.color.RED, border_width=10)
            arcade.draw_line(900, 740, self.world.time, 740, arcade.color.RED, border_width=10)
            arcade.draw_line(900, 760, self.world.time, 760, arcade.color.RED, border_width=10)
            arcade.draw_text("Score : " + str(self.world.all_score), 50, 740, arcade.color.BLACK, 20, 2000)

        if self.world.state == 1:
            self.background_2.draw()
            self.background_3.draw()

    def on_key_press(self, key, key_modifiers):
        if not self.world.is_started() and self.world.state != 3:
            self.world.start()
        if self.world.state == 3 and key == arcade.key.ENTER:
            self.world.reset()
            self.world.state = 1
        self.world.on_key_press(key, key_modifiers)


def main():
    window = Window(SCREEN_WIDTH, SCREEN_HEIGHT)
    arcade.set_window(window)
    arcade.run()


if __name__ == '__main__':
    main()
