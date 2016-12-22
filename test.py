
from random import randint, random
class Table:
    def __init__(self,world):
        self.tab = [
                [0,0,0,0,0],
                [0,0,0,0,0],
                [0,0,0,0,0],
                [0,0,0,0,0],
                [0,0,0,0,0],
                ]
        self.chk_merge = [
                [0,0,0,0,0],
                [0,0,0,0,0],
                [0,0,0,0,0],
                [0,0,0,0,0],
                [0,0,0,0,0],
                ]
        self.full = False;
        self.move_handle = TableMoveHandle()
        self.world = world
        self.random_spawn()

    def animate(self,dir):
        while self.move(dir):
            pass
        # self.random_spawn()
        # for i in self.tab:
        #     for j in i:
        #         print(j ,end="")
        #     print()
        self.cls_chk_merge()

    def check_full(self):
        for i in self.tab:
            for j in i:
                if j == 0:
                    return False
        return True

    def print_table(self):
        for i in self.tab:
            for j in i:
                print(j ,end="")
            print()

    def check_over(self):
        return self.check_full and not self.can_move

    def check_win(self):
        for i in range(5):
            for j in range(5):
                if(self.tab[i][j] == 2048):
                    print(self.tab[i][j])
                    return True
        return False

    def cls_chk_merge(self):
        for i in range(5):
            for j in range(5):
                self.chk_merge[i][j] = 0

    def can_move(self):
        for i in range(5):
            for j in range(5):
                if(i>0):
                    if(self.tab[i][j] == self.tab[i-1][j]):
                        return True
                if(i < 4):
                    if(self.tab[i][j] == self.tab[i+1][j]):
                        return True
                if(j > 0):
                    if(self.tab[i][j] == self.tab[i][j-1]):
                        return True
                if(j < 4):
                    if(self.tab[i][j] == self.tab[i][j+1]):
                        return True
        return False


    def random_spawn(self):
        if self.check_full():
            self.full = True
            return
        x = randint(0,4)
        y = randint(0,4)
        while self.tab[x][y] != 0:
            x = randint(0,4)
            y = randint(0,4)

        self.tab[x][y] = 2
        self.world.grid_handle.add_card(x,y,2)


    def move(self,dir):
        return self.move_handle.move(self.tab,dir,self.chk_merge,self.world.grid_handle)

class TableMoveHandle:
    def __init__(self):
        self.direction = {"left":self.move_up,"right":self.move_down,"down":self.move_left,"up":self.move_right}

    def move(self,tab,dir,chk_merge,grid_handle):
        self.is_moved = False
        try:
            j = 0
            i = 0
            while i < 5:
                while j < 5:
                    j = self.direction[dir](tab,i,j,chk_merge,grid_handle)
                    j += 1
                i += 1
                j = 0
        except:
            pass
        return self.is_moved

    def move_right(self,tab,i,j,chk_merge,grid_handle):
        if tab[i][4-j] != 0:
            if j > 0 and tab[i][5-j] == 0:
                tab[i][5-j] = tab[i][4-j]
                tab[i][4-j] = 0
                chk_merge[i][5-j] = chk_merge[i][4-j]
                chk_merge[i][4-j] = 0
                grid_handle.change_pos(i,4-j,'right',False)
                self.is_moved = True
            elif j > 0  and tab[i][5-j] == tab[i][4-j] and chk_merge[i][4-j] == 0 and chk_merge[i][5-j] == 0:
                tab[i][5-j] *=2
                tab[i][4-j] = 0
                chk_merge[i][5-j] = 1
                grid_handle.change_pos(i,4-j,'right',True)
                self.is_moved = True
        return j;


    def move_left(self,tab,i,j,chk_merge,grid_handle):
        if tab[i][j] != 0:
            if j > 0 and tab[i][j-1] == 0:
                tab[i][j-1] = tab[i][j]
                tab[i][j] = 0
                chk_merge[i][j-1] = chk_merge[i][j]
                chk_merge[i][j] = 0
                grid_handle.change_pos(i,j,'left',False)
                self.is_moved = True
            elif j > 0 and tab[i][j-1] == tab[i][j] and chk_merge[i][j] == 0 and chk_merge[i][j-1] == 0:
                tab[i][j-1] *=2
                tab[i][j] = 0
                chk_merge[i][j-1] = 1
                grid_handle.change_pos(i,j,'left',True)
                self.is_moved = True
        return j;

    def move_up(self,tab,i,j,chk_merge,grid_handle):
        if tab[j][i] != 0:
            if j > 0 and tab[j-1][i] == 0:
                tab[j-1][i] = tab[j][i]
                tab[j][i] = 0
                chk_merge[j-1][i] = chk_merge[j][i]
                chk_merge[j][i] = 0
                grid_handle.change_pos(j,i,'up',False)
                self.is_moved = True
            elif j > 0 and tab[j-1][i] == tab[j][i] and chk_merge[j][i] == 0 and chk_merge[j-1][i] == 0:
                tab[j-1][i] *=2
                tab[j][i] = 0
                chk_merge[j-1][i] = 1
                grid_handle.change_pos(j,i,'up',True)
                self.is_moved = True
        return j;

    def move_down(self,tab,i,j,chk_merge,grid_handle):
        if tab[4-j][i] != 0:
            if j > 0 and tab[5-j][i] == 0:
                tab[5-j][i] = tab[4-j][i]
                tab[4-j][i] = 0
                chk_merge[5-j][i] = chk_merge[4-j][i]
                chk_merge[4-j][i] = 0
                grid_handle.change_pos(4-j,i,'down',False)
                self.is_moved = True
            elif j > 0 and tab[5-j][i] == tab[4-j][i] and chk_merge[4-j][i] == 0 and chk_merge[5-j][i] == 0:
                tab[5-j][i] *=2
                tab[4-j][i] = 0
                chk_merge[5-j][i] = 1
                grid_handle.change_pos(4-j,i,'down',True)
                self.is_moved = True
            #print(j)
        return j;



if __name__ == '__main__':
    table = Table();
    a = 9999
    while a != "0":
        for i in table.tab:
            for j in i:
                print(j ,end="")
            print()
        # print()
        # for i in table.chk_merge:
        #     for j in i:
        #         print(j ,end="")
        #     print()
        # print(table.chk_merge[3][3] == 0)
        a = input()
        table.animate(a)
