import arcade

from models import World
from models import WorldRenderer
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 500


class SpaceGameWindow(arcade.Window):
    def __init__(self, width, height):
        super().__init__(width, height)

        arcade.set_background_color(arcade.color.BLACK)
        self.world = World(width, height)
        self.worldRenderer = WorldRenderer(width,height,self.world)

    def on_draw(self):
        arcade.start_render()
        self.worldRenderer.on_draw()
        # self.bg.draw()

    def animate(self, delta):
        self.world.animate(delta)

    def on_key_press(self, key, key_modifiers):
        self.world.on_key_press(key, key_modifiers)


if __name__ == '__main__':
    window = SpaceGameWindow(SCREEN_WIDTH, SCREEN_HEIGHT)
    arcade.run()
