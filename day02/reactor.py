import click

def is_less_with_margin(val1, val2, margin):
    return val1 < val2 and val1 + margin >= val2

def is_more_with_margin(val1, val2, margin):
    return val1 > val2 and val1 <= val2 + margin

def check_level(data):
    safe = True
    inc = False # Check all decreasing by default
    for i in range(len(data) - 1):
        if i == 0: 
            if is_less_with_margin(data[i], data[i + 1], 3) or is_more_with_margin(data[i], data[i + 1], 3):
                if is_less_with_margin(data[i], data[i + 1], 3):
                    inc = True # Check all increasing
            else:
                safe = False
        else:
            if inc:
                safe = is_less_with_margin(data[i], data[i + 1], 3)
            else:
                safe = is_more_with_margin(data[i], data[i + 1], 3)
        
        if not safe:
            break # break as soon as unsafe detected

    return safe

def part1(file):
    """ Part 1 """
    res = 0

    with open(file) as f:
        for line in f.read().splitlines():
            data = [int(val) for val in line.split(' ')]
            if check_level(data):
                res += 1
    
    print(f'Part 1: Answer is {res}')

def part2(file):
    """ Part 2 """
    res = 0

    with open(file) as f:
        for line in f.read().splitlines():
            data = [int(val) for val in line.split(' ')]
            if check_level(data):
               res += 1
            else:
                # Remove one elem after the other until the check returns safe
                for i in range(len(data)):
                    new_data = [elem for idx, elem in enumerate(data) if idx != i]
                    if check_level(new_data):
                        res += 1
                        break
    
    print(f'Part 2: Answer is {res}')

@click.command()
@click.option('--file', '-f', help='Input file path.')
def main(file):
    part1(file)
    part2(file)

if __name__ == '__main__':
    main()