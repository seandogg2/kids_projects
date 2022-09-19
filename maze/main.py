import re
from enum import IntFlag

import turtle_helpers as th


class Walls(IntFlag):
    top = 1
    bottom = 2
    left = 4
    right = 8


class Room(object):
    def __init__(self, x, y, side=20):
        self.walls = Walls(15)
        self.x = x
        self.y = y
        self.side = side
        self.initialized = False
        self.visited = False

    def set(self, walls):
        if self.initialized:
            print(f'Warning: room ({self.x},{self.y}) has more than one initialization')
        self.walls = Walls(walls)
        self.initialized = True

    def draw(self):
        side = self.side
        bl = (self.x*side, self.y*side)
        tl = (self.x*side, self.y*side+side)
        br = (self.x*side+side, self.y*side)
        tr = (self.x*side+side, self.y*side+side)
        if Walls.left in self.walls:
            th.line(bl, tl)
        if Walls.top in self.walls:
            th.line(tl, tr)
        if Walls.right in self.walls:
            th.line(tr, br)
        if Walls.bottom in self.walls:
            th.line(br, bl)


class Maze(object):
    def __init__(self, side=20):
        self.num_rows = -1
        self.num_cols = -1
        self.side = side
        self.rooms = []

    def init(self, num_rows, num_cols):
        self.num_rows = num_rows
        self.num_cols = num_cols
        self.rooms = []
        for x in range(num_rows):
            row = []
            for y in range(num_cols):
                row.append(Room(x, y, side=self.side))
            self.rooms.append(row)

    def load(self, filename):
        with open(filename, 'rt') as fid:
            txt = fid.read()
            m = re.findall('rows:\s*(\d+),\s*columns:\s*(\d+)', txt)
            assert m, 'row/column clause is required'
            self.init(int(m[0][0]), int(m[0][1]))
            m = re.findall('(\d+)\s*,\s*(\d)\s*:\s*(\d+)', txt)
            assert m, 'did not find any room codes'
            for i in m:
                x = int(i[0])
                y = int(i[1])
                walls = int(i[2])
                assert x < self.num_rows, f'invalid row index {x}'
                assert y < self.num_cols, f'invalid column index {y}'
                assert walls < 16, f'invalid room code at ({x},{y})'
                self.rooms[x][y].set(walls)
            not_initialized = []
            for x in range(self.num_rows):
                for y in range(self.num_cols):
                    if not self.rooms[x][y].initialized:
                        not_initialized.append((x,y))
            if not_initialized:
                print('Warning: the following rooms have not been initialized:')
                for i in not_initialized:
                    print(f'\t{i}')

    def draw(self):
        th.init(0, 0, self.num_rows*self.side, self.num_cols*self.side)
        for x in range(self.num_rows):
            for y in range(self.num_cols):
                self.rooms[x][y].draw()


if __name__ == '__main__':
    th.Jonathan_test()
    #jonathan = Maze()
    #jonathan.load('jonathan1.maze')
    #jonathan.draw()
    #daniel = Maze()
    #daniel.load('charred_ham.maze')
    #daniel.draw()
    input()