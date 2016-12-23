import arcade.key
import arcade
from random import randint, random
from test import Table

class Model:
    def __init__(self, x, y, angle):
        self.x = x
        self.y = y
        self.angle = 0

    def hit(self, other, hit_size):
        return (abs(self.x - other.x) <= hit_size) and (abs(self.y - other.y) <= hit_size)

class ModelSprite(arcade.Sprite):
    def __init__(self, *args, **kwargs):
        self.model = kwargs.pop('model', None)

        super().__init__(*args, **kwargs)

    def sync_with_model(self):
        if self.model:
            self.set_position(self.model.x, self.model.y)
            self.angle = self.model.angle

    def draw(self):
        self.sync_with_model()
        super().draw()


class Card(Model):
    def __init__(self, x, y, pos_x, pos_y, type):
        super().__init__( x, y, 0)
        self.vx = 0
        self.vy = 0
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.type = type
        self.upgrade = False

    def animate(self, delta):
        self.x += self.vx
        self.y += self.vy

class World:

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.grid_handle = GridHandle()
        self.table = Table(self)
        self.can_press = False
        self.spawn = True
        self.q = 'gg'
        self.arrow = Model((290/2)+500,(264/2)+10,0)
        self.delay = 0
        self.win = 0

    def animate(self, delta):
        # print(self.win)
        self.can_press = not self.grid_handle.on_move(delta)
        if(not self.can_press):
            self.delay = 5
        if(self.can_press and self.delay > 0):
            self.delay -= 1
        if(self.can_press and not self.spawn):
            self.table.random_spawn()
            self.spawn = True
        if(self.table.check_win()):
            self.win = 1
            # print('kuy')
        if(self.table.check_over()):
            self.win = -1
        if(self.can_press):
            self.grid_handle.cnt = 0


    def on_key_press(self, key, key_modifiers):
        if key == arcade.key.UP and self.can_press and self.delay == 0:
            if(self.q!='gg'):
                self.table.animate(self.q)
                self.table.print_table()
            self.q = 'up'
            self.arrow.angle = 90
            self.spawn = False;
        elif key == arcade.key.DOWN and self.can_press and self.delay == 0:
            if(self.q!='gg'):
                self.table.animate(self.q)
                self.table.print_table()
                # self.grid_handle.print_grid()
            self.q = "down"
            self.arrow.angle = 270
            self.spawn = False;
        elif key == arcade.key.LEFT and self.can_press and self.delay == 0:
            if(self.q!='gg'):
                self.table.animate(self.q)
                self.table.print_table()
                # self.grid_handle.print_grid()
            self.q = "left"
            self.arrow.angle = 180
            self.spawn = False;
        elif key == arcade.key.RIGHT and self.can_press and self.delay == 0:
            if(self.q!='gg'):
                self.table.animate(self.q)
                self.table.print_table()
                # self.grid_handle.print_grid()
            self.q = "right"
            self.arrow.angle = 0
            self.spawn = False;

class GridHandle():
    def __init__(self):
        self.grid = []
        self.cardType = {}
        for i in range(11) :
            self.cardType[2**(i+1)] = 'assets/'+str(2**(i+1))+'.png'
        self.sprite = []
        self.direction = {'up':[-1,0],'down':[1,0],'left':[0,-1],'right':[0,1]}
        self.cnt = 0

    def add_card(self,x,y,type):
        self.grid.append(Card((x*100)+50,(y*100)+50,x,y,type))
        self.sprite.append(ModelSprite(self.cardType[type],model=self.grid[-1]))
        # print(self.grid[-1].pos_x)

    def upgrade_card(self,x,y):
        i = 0
        tmp = 0
        while(i < len(self.grid)):
            # print('1')
            if(self.grid[i].pos_x == x and self.grid[i].pos_y == y):
                if(self.grid[i].type > tmp):
                    tmp = self.grid[i].type
                del self.grid[i]
                del self.sprite[i]
                i -= 1
            i += 1
        self.add_card(x,y,tmp*2)

    def on_move(self,delta):
        to_ret = False
        i = 0
        while i < len(self.grid) :
            # print('2 '+str(i))
            self.grid[i].animate(delta)
            if((self.grid[i].pos_x*100)+50 != self.grid[i].x or (self.grid[i].pos_y*100)+50 != self.grid[i].y):
                # print((self.grid[i].pos_x,self.grid[i].pos_y,self.grid[i].x,self.grid[i].y))
                if(self.cnt > 50):
                    self.grid[i].x = (self.grid[i].pos_x*100)+50
                    self.grid[i].y = (self.grid[i].pos_y*100)+50
                if((self.grid[i].pos_x*100)+50 == self.grid[i].x):
                    self.grid[i].vx = 0
                if((self.grid[i].pos_y*100)+50 == self.grid[i].y):
                    self.grid[i].vy = 0
                self.cnt += 1
                to_ret = True
            else :
                self.grid[i].vx = 0
                self.grid[i].vy = 0
                if(self.grid[i].upgrade):
                    # print(self.grid[i].pos_x)
                    self.upgrade_card(self.grid[i].pos_x,self.grid[i].pos_y)
                    i -= 1
            i += 1
        return to_ret

    def print_grid(self):
        for i in range(5):
            for j in range(5):
                found = True
                for k in self.grid :
                    if(k.pos_x == i and k.pos_y == j):
                        found = False
                        print(k.type,end=' ')
                        break;
                if(found):
                    print(0,end=' ')
            print()


    def change_pos(self,x,y,dir,upgrade):
        for i in range(len(self.grid)):
            if(self.grid[i].pos_x == x and self.grid[i].pos_y == y):
                self.grid[i].pos_x += self.direction[dir][0]
                self.grid[i].pos_y += self.direction[dir][1]
                self.grid[i].vx += self.direction[dir][0]*10
                self.grid[i].vy += self.direction[dir][1]*10
                self.grid[i].upgrade = upgrade


class WorldRenderer():
    def __init__(self,width,height,world):
        self.width = width
        self.height = height
        self.world = world
        self.bg = arcade.Sprite('assets/bg.png')
        self.win = arcade.Sprite('assets/win.png')
        self.lose = arcade.Sprite('assets/lose.png')
        self.bg.set_position(width/2,height/2)
        self.win.set_position(width/2,height/2)
        self.lose.set_position(width/2,height/2)
        self.arrow_sprite = ModelSprite('assets/arrow.png',model=world.arrow)

    def on_draw(self):
        self.bg.draw()
        for i in self.world.grid_handle.sprite :
            i.draw()
        if(self.world.q != 'gg'):
            self.arrow_sprite.draw()
        if(self.world.win == 1):
            self.win.draw()
        if(self.world.win == -1):
            self.lose.draw()

if __name__ == '__main__':
    pass
