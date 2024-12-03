import click
import re

def sum_all_mul(txt):
    all_mul = []
    # Find all mul(X*Y)
    mul_list = re.findall(r"mul\([0-9]+,[0-9]+\)", txt)
    for mul in mul_list:
        # Find X and Y
        numbers = re.findall(r"[0-9]+", mul)
        if len(numbers) == 2:
            # Multiply X*Y
            all_mul.append(int(numbers[0]) * int(numbers[1]))
    return sum(all_mul)

def part1(file):
    """ Part 1 """
    with open(file) as f:
        txt = f.read()
    
    res = sum_all_mul(txt)
    print(f'Part 1: Answer is {res}')

def part2(file):
    """ Part 2 """
    with open(file) as f:
        txt = f.read()
    
    res = 0
    dont_split = txt.split("don't()")
    for idx, elem in enumerate(dont_split):
        if idx == 0:
            # First part without don't is enabled
            res += sum_all_mul(elem)
        
        do_split = elem.split("do()")
        if len(do_split) > 1:
            # Part before do is disabled
            # All parts after do is enabled
            res += sum_all_mul(''.join(do_split[1:]))
    
    print(f'Part 2: Answer is {res}')

@click.command()
@click.option('--file', '-f', help='Input file path.')
def main(file):
    part1(file)
    part2(file)

if __name__ == '__main__':
    main()