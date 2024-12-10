import click
import numpy as np 

class Grid():
    directions = [(-1, 0), (1, 0), (0, 1), (0, -1)] # nord, sud, est, west

    def __init__(self, grid: list):
        self.grid_map = np.array(grid)
        self.grid_size = self.grid_map.shape

    def __str__(self):
        return f"{self.grid_map}\n Size {self.grid_size}"
    
    def get_positions(self, value):
        return list(zip(*np.where(self.grid_map == value)))
    
    def get_value(self, position: tuple):
        return self.grid_map[position]    
    
    def is_in_grid(self, position: tuple):
        in_grid = False
        if position[0] >= 0 and position[1] >= 0 and \
            position[0] < self.grid_size[0] and position[1] < self.grid_size[1]:
            in_grid = True
        return in_grid
    
def get_next_pos(grid: Grid, positions: list):
    next_pos = list()
    for position in positions:
        pos_value = grid.get_value(position)
        for d in grid.directions:
            new_pos = tuple(map(lambda i, j: i + j, position, d))
            if grid.is_in_grid(new_pos):
                if grid.get_value(new_pos) == pos_value + 1:
                    next_pos.append(new_pos)
    return next_pos
    
def part1(grid: Grid, start_pos: tuple):
    """ Part 1 """
    positions = list()
    positions.append(start_pos)
    for _ in range(9):
        next_pos = get_next_pos(grid, positions)
        positions = list(set(next_pos))
    return len(positions)

def part2(grid: Grid, start_pos: tuple):
    """ Part 2: All paths taken into account (remove set conversion of part1) """
    positions = list()
    positions.append(start_pos)
    for _ in range(9):
        positions = get_next_pos(grid, positions)
    return len(positions)

@click.command()
@click.option('--file', '-f', help='Input file path.')
def main(file):
    # Read file
    input_table = list()
    with open(file) as f:
        for line in f.read().splitlines():
            input_table.append([int(elem) for elem in line])
    
    grid = Grid(input_table)
    trailheads = grid.get_positions(0)

    res1 = 0
    res2 = 0
    for trailhead in trailheads:
        res1 += part1(grid, trailhead)
        res2 += part2(grid, trailhead)
    print(f'Part 1: Answer is {res1}')
    print(f'Part 2: Answer is {res2}')


if __name__ == '__main__':
    main()