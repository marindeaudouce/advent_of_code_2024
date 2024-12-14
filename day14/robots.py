import click
import re
from PIL import Image
import numpy as np

SECONDS = 100
GRID_SIZE = (101, 103)

def part1(robots: list):
    """ Part 1 """
    # Compute final positions of each robot
    final_pos = list()
    for robot in robots:
        x_pos = (robot[0] + robot[2] * SECONDS)%GRID_SIZE[0]
        y_pos = (robot[1] + robot[3] * SECONDS)%GRID_SIZE[1]
        final_pos.append((x_pos,y_pos))

    # Compute the number of robot per cadran
    cadran = [0, 0, 0, 0]
    for pos in final_pos:
        if pos[0] < GRID_SIZE[0]//2:
            if pos[1] < GRID_SIZE[1]//2:
                # top left cadran
                cadran[0] += 1
            elif pos[1] > GRID_SIZE[1]//2:
                # bottom left cadran
                cadran[2] += 1
        elif pos[0] > GRID_SIZE[0]//2:
            if pos[1] < GRID_SIZE[1]//2:
                # top right cadran
                cadran[1] += 1
            elif pos[1] > GRID_SIZE[1]//2:
                # bottom right cadran
                cadran[3] += 1

    # Multiply all the cadran together
    res = 1
    for value in cadran:
        res *= value

    return res

def part2(robots: list):
    """ Part 2 """
    black = (0, 0, 0)
    white = (255, 255, 255)
    for second in range(8000, 9000):
        final_pos = list()
        for robot in robots:
            x_pos = (robot[0] + robot[2] * second)%GRID_SIZE[0]
            y_pos = (robot[1] + robot[3] * second)%GRID_SIZE[1]
            final_pos.append((x_pos,y_pos))
        
        pixels = list()
        for posx in range(GRID_SIZE[0]):
            line = list()
            for posy in range(GRID_SIZE[1]):
                if tuple((posx, posy)) in final_pos:
                    line.append(white)
                else:
                    line.append(black)
            pixels.append(line)
        
        img_array = np.array(pixels, dtype=np.uint8)
        new_image = Image.fromarray(img_array)
        new_image.save(f'output8/seconds_{second}.png')

@click.command()
@click.option('--file', '-f', help='Input file path.')
def main(file):
    # Read file
    robots = list()
    with open(file) as f:
        for line in f.read().splitlines():
            input = [int(num) for num in re.findall(r'-?\d+', line)]
            robots.append(input)

    res = part1(robots)
    print(f'Part 1: Answer is {res}')

    part2(robots)

if __name__ == '__main__':
    main()