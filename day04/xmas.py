import click
from enum import Enum

class Direction(Enum):
    NW = 0
    N = 1
    NE = 2
    W = 3
    C = 4
    E = 5
    SW = 6
    S = 7
    SE = 8

def get_opposite_dir(direction: Direction):
    opposite_dir = Direction.C
    if direction == Direction.NW:
        opposite_dir = Direction.SE
    elif direction == Direction.N:
        opposite_dir = Direction.S
    elif direction == Direction.NE:
        opposite_dir = Direction.SW
    elif direction == Direction.W:
        opposite_dir = Direction.E
    elif direction == Direction.E:
        opposite_dir = Direction.W
    elif direction == Direction.SW:
        opposite_dir = Direction.NE
    elif direction == Direction.S:
        opposite_dir = Direction.N
    elif direction == Direction.SE:
        opposite_dir = Direction.NW
    return opposite_dir

def is_not_cardinal(direction: Direction):
    is_not_cardinal = False
    if direction == Direction.NW or direction == Direction.SE or \
        direction == Direction.SW or direction == Direction.NE:
        is_not_cardinal = True
    return is_not_cardinal


class Letter():
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def __str__(self):
        return f'({self.x},{self.y})'
    
    def is_close(self, elem: 'Letter'):
        close = False
        dir = Direction.C
        if elem.x == self.x: # Check left, right
            if elem.y == self.y + 1:
                dir = Direction.S
                close = True
            elif elem.y == self.y - 1:
                dir = Direction.N
                close = True
        elif elem.y == self.y: # Check bottom up
            if elem.x == self.x + 1:
                dir = Direction.E
                close = True
            elif elem.x == self.x -1:
                dir = Direction.W
                close = True
        elif elem.x == self.x + 1: # Check diag
            if elem.y == self.y + 1:
                dir = Direction.SE
                close = True
            elif elem.y == self.y - 1:
                dir = Direction.NE
                close = True
        elif elem.x == self.x - 1: # Check diag
            if elem.y == self.y + 1:
                dir = Direction.SW
                close = True
            elif elem.y == self.y - 1:
                dir = Direction.NW
                close = True
        return close, dir
    
    def is_close_w_dir(self, elem: 'Letter', direction: Direction):
        close = False
        if direction == Direction.NW:
            close = (elem.x == self.x - 1 and elem.y == self.y - 1)
        elif direction == Direction.N:
            close = (elem.x == self.x and elem.y == self.y - 1)
        elif direction == Direction.NE:
            close = (elem.x == self.x + 1 and elem.y == self.y - 1)
        elif direction == Direction.W:
            close = (elem.x == self.x - 1 and elem.y == self.y)
        elif direction == Direction.E:
            close = (elem.x == self.x + 1 and elem.y == self.y)
        elif direction == Direction.SW:
            close = (elem.x == self.x - 1 and elem.y == self.y + 1)
        elif direction == Direction.S:
            close = (elem.x == self.x and elem.y == self.y + 1)
        elif direction == Direction.SE:
            close = (elem.x == self.x + 1 and elem.y == self.y + 1)
        return close 


def part1(file):
    """ Part 1 """
    res = 0

    # Read input table
    input_table = []
    with open(file) as f:
        for line in f.read().splitlines():
            elem_list = [elem for elem in line]
            input_table.append(elem_list)
    
    # Get every X, M, A, and S coordinates
    idx_X = []
    idx_M = []
    idx_A = []
    idx_S = []
    for idx_line, elem_line in enumerate(input_table):
        for idx_col, elem_col in enumerate(elem_line):
            if elem_col == 'X':
                idx_X.append(Letter(idx_line, idx_col))
            elif elem_col == 'M':
                idx_M.append(Letter(idx_line, idx_col))
            elif elem_col == 'A':
                idx_A.append(Letter(idx_line, idx_col))
            elif elem_col == 'S':
                idx_S.append(Letter(idx_line, idx_col))
    
    # Check if any XMAS
    for x in idx_X:
        for m in idx_M:
            is_close, direction = m.is_close(x)
            if is_close:
                for a in idx_A:
                    if a.is_close_w_dir(m, direction):
                        for s in idx_S: 
                            if s.is_close_w_dir(a, direction):
                                res += 1
    
    print(f'Part 1: Answer is {res}')

def part2(file):
    """ Part 2 """
    res = 0

    # Read input table
    input_table = []
    with open(file) as f:
        for line in f.read().splitlines():
            elem_list = [elem for elem in line]
            input_table.append(elem_list)
    
    # Get every M, A, and S coordinates
    idx_M = []
    idx_A = []
    idx_S = []
    for idx_line, elem_line in enumerate(input_table):
        for idx_col, elem_col in enumerate(elem_line):
            if elem_col == 'M':
                idx_M.append(Letter(idx_line, idx_col))
            elif elem_col == 'A':
                idx_A.append(Letter(idx_line, idx_col))
            elif elem_col == 'S':
                idx_S.append(Letter(idx_line, idx_col))
        
    # Check if any X-MAS
    MAS_nbr = 0
    for a in idx_A:
        for m in idx_M:
            is_close, direction = a.is_close(m)
            if is_close and is_not_cardinal(direction):
                opposite_dir = get_opposite_dir(direction)
                for s in idx_S:
                    if a.is_close_w_dir(s, opposite_dir):
                        MAS_nbr += 1
        if MAS_nbr == 2:
            res += 1
        MAS_nbr = 0        

    print(f'Part 2: Answer is {res}')

@click.command()
@click.option('--file', '-f', help='Input file path.')
def main(file):
    # Each part take ages to run ...
    part1(file)
    part2(file)

if __name__ == '__main__':
    main()