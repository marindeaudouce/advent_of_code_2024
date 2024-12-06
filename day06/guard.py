import click
import re

def part1(file):
    """ Part 1 """ 
    guard = tuple()
    walls = list()
    grid_size = tuple()
    with open(file) as f:
        for x, line in enumerate(f.read().splitlines()):
            guard_y = line.find('^')
            if guard_y != -1:
                guard = (x, guard_y)
            walls_y = [x.start() for x in re.finditer('#', line)]
            if walls_y:
                walls.extend([(x, w) for w in walls_y])
        grid_size = x, len(line)
    
    directions = [(-1, 0), (0, 1), (1, 0), (0, -1)] # nord, est, sud, west
    hit = 0
    visited_pos = list()
    while not (guard[0] == 0 or guard[0] == grid_size[0] or guard[1] == 0 or guard[1] == grid_size[1]):
        next_pos = tuple(map(lambda i, j: i + j, guard, directions[hit%4]))
        if next_pos not in walls:
            visited_pos.append(next_pos)
            guard = next_pos
        else:
            hit += 1
          
    print(f'Part 1: Answer is {len(set(visited_pos))}')

def part2(file):
    """ Part 2 """
    res = 0
    print(f'Part 2: Answer is {res}')

@click.command()
@click.option('--file', '-f', help='Input file path.')
def main(file):
    part1(file)
    part2(file)

if __name__ == '__main__':
    main()