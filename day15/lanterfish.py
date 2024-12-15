import click
import numpy as np

class Warehouse():
    directions = [(-1, 0), (1, 0), (0, 1), (0, -1)] # nord, sud, est, west

    def __init__(self, grid: list):
        self.grid_map = np.array(grid)
        self.grid_size = self.grid_map.shape
        self.robot = self.get_positions('@')[0]

    def __str__(self):
        return f"{self.grid_map}\n Size {self.grid_size}"
    
    def get_positions(self, value):
        return list(zip(*np.where(self.grid_map == value)))
    
    def get_value(self, position: tuple):
        return self.grid_map[position]    
    
    def get_grid_size(self):
        return self.grid_size 
    
    def get_boxes(self):
        return self.get_positions('O')
    
    def get_robot(self):
        return self.robot

    def is_wall(self, position: tuple):
        return self.grid_map[position] == '#' 
    
    def is_box(self, position: tuple):
        return self.grid_map[position] == 'O'
    
    def compute_gps(self):
        gps_list = list()
        for xbox, ybox in self.get_boxes():
            gps = xbox * 100 + ybox
            gps_list.append(gps)
        return gps_list
    
    def map_directions(self, arrow: str):
        dir = None
        if arrow == '^':
            dir = self.directions[0]
        elif arrow == 'v':
            dir = self.directions[1]
        elif arrow == '>':
            dir = self.directions[2]
        elif arrow == '<':
            dir = self.directions[3]
        return dir
    
    def move_robot(self, dir: tuple):
        new_pos = tuple(map(lambda i, j: i + j, self.robot, dir))
        if not self.is_wall(new_pos):
            if not self.is_box(new_pos):
                # print(f"No wall, no box, move the robot")
                self.robot = new_pos
            else: 
                next_pos = tuple(map(lambda i, j: i + j, new_pos, dir))
                boxes_to_move = list()
                boxes_to_move.append(new_pos)
                while self.is_box(next_pos):
                    # print(f"Box behind a box")
                    boxes_to_move.append(next_pos)
                    next_pos = tuple(map(lambda i, j: i + j, next_pos, dir))
        
                if not self.is_wall(next_pos):
                    # print(f"Robot moves with {len(boxes_to_move)} boxes")
                    self.grid_map[boxes_to_move[0]] = '.'
                    self.grid_map[tuple(map(lambda i, j: i + j, boxes_to_move[-1], dir))] = 'O'
                    self.robot = new_pos
                # else:
                #     print(f"Cannot move because of a wall")
        # else:
            # print(f"Cannot move because of a wall")


    
@click.command()
@click.option('--file', '-f', help='Input file path.')
def main(file):
    # Read file
    input_table = list()
    moves = list()
    is_grid = True
    with open(file) as f:
        for line in f.read().splitlines():
            if line == '':
                is_grid = False
            elif is_grid:
                input_table.append([elem for elem in line])
            else:
                moves.extend([elem for elem in line])

    grid = Warehouse(input_table)

    for move in moves:
        dir = grid.map_directions(move)
        grid.move_robot(dir)
    
    gps_list = grid.compute_gps()
    print(f'Part 1: Answer is {sum(gps_list)}')


if __name__ == '__main__':
    main()