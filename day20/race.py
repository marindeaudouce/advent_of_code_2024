import click
import numpy as np

class Grid():
    directions = [(0, 1), (0, -1), (-1, 0), (1, 0)] # nord, sud, est, west

    def __init__(self, grid: list):
        self.grid_map = np.array(grid)
        self.grid_size = self.grid_map.shape
        self.start_pos = self.get_positions('S')[0]
        self.end_pos = self.get_positions('E')[0]
        self.grid_map[self.end_pos] = '.'
        self.grid_map[self.start_pos] = '.'

    def __str__(self):
        return f"{self.grid_map}\n Size {self.grid_size}"
    
    def get_positions(self, value):
        return list(zip(*np.where(self.grid_map == value)))
    
    def get_value(self, position: tuple):
        return self.grid_map[position]    
    
    def get_grid_size(self):
        return self.grid_size

    def is_wall(self, position: tuple):
        return self.grid_map[position] == '#'
    
    def is_path(self, position: tuple):
        return self.grid_map[position] == '.'
    
    def increase_position(self, position: tuple, direction: tuple):
        return tuple(map(lambda i, j: i + j, position, direction))
    
    def update_map(self, position: tuple, value: str):
        self.grid_map[position] = value
    
    def shuffle_direction(self):
        first_elem = self.directions[0]
        self.directions = self.directions[1:]
        self.directions.append(first_elem)
    
    def compute_race_time(self):
        picosec = 0
        current_pos = self.start_pos
        last_pos = None
        while current_pos != self.end_pos:
            for direction in self.directions:
                new_pos = self.increase_position(current_pos, direction)
                if self.is_path(new_pos) and new_pos != last_pos:
                    picosec += 1
                    last_pos = current_pos
                    current_pos = new_pos
                    break
            if current_pos == self.start_pos:
                print("Loop")
                break
        return picosec
    
    def compute_cheat_pos(self):
        cheat_pos = list()
        for line_idx, line in enumerate(self.grid_map):
            for idx, elem in enumerate(line):
                if idx != 0 and idx != len(line) - 1:
                    if elem == '#' and line[idx - 1] == '.' and line[idx + 1] == '.':
                        cheat_pos.append((line_idx, idx))
        for col_idx, col in enumerate(self.grid_map.T):
            for idx, elem in enumerate(col):
                if idx != 0 and idx != len(col) - 1:
                    if elem == '#' and col[idx - 1] == '.' and col[idx + 1] == '.':
                        cheat_pos.append((idx, col_idx))
        return cheat_pos

@click.command()
@click.option('--file', '-f', help='Input file path.')
def main(file):
    # Read file
    input_table = list()
    with open(file) as f:
        for line in f.read().splitlines():
            input_table.append([elem for elem in line])

    grid = Grid(input_table)
    ref_race_time = grid.compute_race_time()
    print(f"Race time: {ref_race_time} picoseconds")
    cheat_pos = grid.compute_cheat_pos()
    print(f"Number of cheat position: {len(cheat_pos)}")
    for pos in cheat_pos:
        grid.update_map(pos, '.')
        time = 0
        while time == 0 or time == ref_race_time:
            time = grid.compute_race_time()
            grid.shuffle_direction()
        print(f"Time saved : {pos}, {ref_race_time - time}")
        grid.update_map(pos, '#')

    res = 0
    print(f'Part 1: Answer is {res}')


if __name__ == '__main__':
    main()