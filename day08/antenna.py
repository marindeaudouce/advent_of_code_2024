import click
import re
import itertools

def is_in_grid(grid_size: tuple, position: tuple):
    in_grid = False
    if position[0] >= 0 and position[1] >= 0 and \
        position[0] <= grid_size[0] and position[1] <= grid_size[1]:
        in_grid = True
    return in_grid

def part1(antennas: dict, grid_size: tuple):
    """ Part 1 """ 
    antinodes = []
    for pos in antennas.values():
        pairs = list(itertools.combinations(pos, 2))
        for pair in pairs:
            local_antinodes = []
            offset = tuple(map(lambda i, j: i - j, pair[1], pair[0]))
            local_antinodes.append(tuple(map(lambda i, j: i - j, pair[0], offset)))
            local_antinodes.append(tuple(map(lambda i, j: i + j, pair[1], offset)))
            for antinode in local_antinodes:
                if is_in_grid(grid_size, antinode):
                    antinodes.append(antinode)
    
    print(f'Part 1: Answer is {len(set(antinodes))}')

def part2(antennas: dict, grid_size: tuple):
    """ Part 2 """
    antinodes = []
    for pos in antennas.values():
        antinodes.extend(pos) # antennas now counts as antinodes too
        pairs = list(itertools.combinations(pos, 2))
        for pair in pairs:
            offset = tuple(map(lambda i, j: i - j, pair[1], pair[0]))
            # antinodes in direction of first pair
            antinode = tuple(map(lambda i, j: i - j, pair[0], offset))
            while is_in_grid(grid_size, antinode):
                antinodes.append(antinode)
                antinode = tuple(map(lambda i, j: i - j, antinode, offset))

            # antinodes in direction of second pair
            antinode = tuple(map(lambda i, j: i + j, pair[1], offset))
            while is_in_grid(grid_size, antinode):
                antinodes.append(antinode)
                antinode = tuple(map(lambda i, j: i + j, antinode, offset))

    print(f'Part 2: Answer is {len(set(antinodes))}')

@click.command()
@click.option('--file', '-f', help='Input file path.')
def main(file):
    antennas = dict()
    grid_size = tuple()
    with open(file) as f:
        for x, line in enumerate(f.read().splitlines()):
            for ant in re.finditer(r"[0-9]|[a-z]|[A-Z]", line):
                if ant.group() in antennas.keys(): 
                    # if antenna with the same frequency already present, append new position
                    positions = antennas.get(ant.group())
                    positions.append((x, ant.start()))
                    antennas[ant.group()] = positions
                else:
                    antennas[ant.group()] = [(x, ant.start())]
        grid_size = x, len(line) - 1 

    part1(antennas, grid_size)
    part2(antennas, grid_size)

if __name__ == '__main__':
    main()