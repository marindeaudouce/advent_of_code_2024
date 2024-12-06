import click
import re

DIRECTIONS = [(-1, 0), (0, 1), (1, 0), (0, -1)] # nord, est, sud, west

def is_in_grid(grid_size: tuple, position: tuple):
    in_grid = False
    if position[0] > 0 and position[1] > 0 and \
        position[0] < grid_size[0] and position[1] < grid_size[1]:
        in_grid = True
    return in_grid

def part1(guard: tuple, walls: list, grid_size: tuple):
    """ Part 1 """  
    hit = 0
    visited_pos = [guard]
    while is_in_grid(grid_size, guard):
        next_pos = tuple(map(lambda i, j: i + j, guard, DIRECTIONS[hit%4]))
        if next_pos not in walls:
            visited_pos.append(next_pos)
            guard = next_pos
        else:
            hit += 1
          
    print(f'Part 1: Answer is {len(set(visited_pos))}')

def compute_loop_pos(last_hits: list, hit_pos: tuple):
    loop_pos = list()
    hit = len(last_hits)
    if hit > 3:
        for idx in range(hit//4):
            if hit%4 == 0: # if west
                if hit_pos[1] < last_hits[idx*4 + 0][1]:
                    loop_pos.append((hit_pos[0], last_hits[idx*4 + 0][1] - 1))
            if hit%4 == 2: # if est
                if hit_pos[1] > last_hits[idx*4 + 2][1]:
                    loop_pos.append((hit_pos[0], last_hits[idx*4 + 2][1] + 1))
            if hit%4 == 1: # if nord
                if hit_pos[0] < last_hits[idx*4 + 1][0]:
                    loop_pos.append((last_hits[idx*4 + 1][0] - 1, hit_pos[1]))
            if hit%4 == 3: # if sud
                if hit_pos[0] > last_hits[idx*4 + 3][0]:
                    loop_pos.append((last_hits[idx*4 + 3][0] + 1, hit_pos[1]))
    return loop_pos

def part2(guard: tuple, walls: list, grid_size: tuple):
    """ Part 2 """
    hit = 0
    visited_pos = [guard]
    last_hits = list()
    loop_pos = list()
    while is_in_grid(grid_size, guard):
        next_pos = tuple(map(lambda i, j: i + j, guard, DIRECTIONS[hit%4]))
        if next_pos not in walls:
            visited_pos.append(next_pos)
            guard = next_pos
        else:
            last_hits.append(next_pos)
            hit = len(last_hits)
            loop_pos.extend(compute_loop_pos(last_hits, next_pos))
    last_hits.append(guard)
    loop_pos.extend(compute_loop_pos(last_hits, guard))
    # print(len(loop_pos), loop_pos)
    print(f'Part 2: Answer is {len(set(loop_pos))}') # Wrong answer

@click.command()
@click.option('--file', '-f', help='Input file path.')
def main(file):
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
        grid_size = x, len(line) - 1  
    
    part1(guard, walls, grid_size)
    part2(guard, walls, grid_size)

if __name__ == '__main__':
    main()