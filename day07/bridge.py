import click
from itertools import product

def part1(file):
    """ Part 1 """ 
    calibration = 0
    inputs = dict()
    with open(file) as f:
        for line in f.read().splitlines():
            result, numbers = line.split(':')
            inputs[int(result)] = [int(num) for num in numbers.strip().split(' ')]

    for res, num in inputs.items():
        operations = list(product(['+', '*'], repeat=len(num)-1))
        for op in operations:
            r = num[0]
            for idx, n in enumerate(num[1:]):
                r = eval(f'{r}{op[idx]}{n}')
            if r == res:
                calibration += r
                break
                
    print(f'Part 1: Answer is {calibration}')

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