
from space import ModelSprite
import arcade
class WorldRenderer():
    def __init__(self,width,height):
        self.width = width
        self.height = height
        self.bg = arcade.Sprite('assets/bg.png')
        self.bg.set_position(width/2,height/2)

    def on_draw(self):
        self.bg.draw()
