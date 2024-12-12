import click
import numpy as np
from string import ascii_uppercase

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
    
    def get_grid_size(self):
        return self.grid_size
    
    def is_in_grid(self, position: tuple):
        in_grid = False
        if position[0] >= 0 and position[1] >= 0 and \
            position[0] < self.grid_size[0] and position[1] < self.grid_size[1]:
            in_grid = True
        return in_grid
    
    def is_close(self, positions: tuple):
        close = False
        for dir in self.directions:
            new_pos = tuple(map(lambda i, j: i + j, positions[0], dir))
            if new_pos == positions[1]:
                close = True
                break
        return close
    
    def get_close(self, position: tuple, elem):
        close_pos = list()
        for dir in self.directions:
            new_pos = tuple(map(lambda i, j: i + j, position, dir))
            if self.is_in_grid(new_pos):
                if self.grid_map[new_pos] == elem:
                    close_pos.append(new_pos)
        return close_pos
    
    def get_cluster(self, positions: list, start_pos, elem):
        visited_pos = set()
        visited_pos.add(start_pos)
        close_pos = set(self.get_close(start_pos, elem))
        while close_pos:
            new_close = list()
            for pos in close_pos:
                visited_pos.add(pos)
                new_close.extend(self.get_close(pos, elem))
            close_pos = set(new_close) - visited_pos
        return list(visited_pos)

    
@click.command()
@click.option('--file', '-f', help='Input file path.')
def main(file):
    # Read file
    input_table = list()
    with open(file) as f:
        for line in f.read().splitlines():
            input_table.append([elem for elem in line])
    
    grid = Grid(input_table)
    regions = dict() # Letter: list of areas 
    for char in ascii_uppercase:
        pos_char = grid.get_positions(char)
        # Compute area and number of clusters
        if pos_char:
            visited_pos = list()
            clusters = list()
            if len(pos_char) > 1:
                start_pos = pos_char[0]
                close_pos = grid.get_cluster(pos_char, start_pos, char)
                clusters.append(close_pos)
                print(f"Region of plant {char} have area {len(close_pos)}")
                not_visited = list(set(pos_char)-set(close_pos))
                visited_pos.extend(close_pos)
                while not_visited:
                    new_visit_pos = grid.get_cluster(not_visited, not_visited[0], char)
                    clusters.append(new_visit_pos)
                    print(f"Region of plant {char} have area {len(new_visit_pos)}")
                    visited_pos.extend(new_visit_pos)
                    not_visited = list(set(pos_char)-set(visited_pos))
                regions[char] = clusters
            else: # stand alone plant
                regions[char] = [pos_char]
                print(f"Region of plant {char} have area 1")
    
    # Compute perimeter
    prices = list() # (area, perameter)
    for region, clusters in regions.items():
        for cluster in clusters:
            perimeter = 0
            if len(cluster) > 1:
                for pos in cluster:
                    close_pos = grid.get_close(pos, region)
                    perimeter += 4 - len(close_pos)
                prices.append((len(cluster), perimeter))
            else: # stand alone plant
                prices.append((1, 4))
                
    res1 = 0
    for price in prices:
        res1 += price[0] * price[1]
    print(f'Part 1: Answer is {res1}')


if __name__ == '__main__':
    main()