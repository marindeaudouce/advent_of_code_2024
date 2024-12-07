import click
from itertools import product
from enum import Enum

class Operations(Enum):
    ADD = 0
    MUL = 1
    CONCAT = 2

def apply_operation(operation: Operations, operand1: int, operand2: int):
    result = None
    if operation == Operations.ADD:
        result = operand1 + operand2
    elif operation == Operations.MUL:
        result = operand1 * operand2
    elif operation == Operations.CONCAT:
        result = int(str(operand1) + str(operand2))
    return result

def compute_total_calibration(inputs: dict, operation: list): 
    total = 0
    for result, num in inputs.items():
        operations = list(product(operation, repeat=len(num)-1))
        for op in operations:
            temp_res = num[0]
            for idx, n in enumerate(num[1:]):
                temp_res = apply_operation(op[idx], temp_res, n)
            if temp_res == result:
                total += result
                break
    return total

@click.command()
@click.option('--file', '-f', help='Input file path.')
def main(file):
    inputs = dict()
    with open(file) as f:
        for line in f.read().splitlines():
            result, numbers = line.split(':')
            inputs[int(result)] = [int(num) for num in numbers.strip().split(' ')]
    
    part1_total = compute_total_calibration(inputs, [Operations.ADD, Operations.MUL])
    print(f'Part 1: Answer is {part1_total}')

    part2_total = compute_total_calibration(inputs, [Operations.ADD, Operations.MUL, Operations.CONCAT])
    print(f'Part 2: Answer is {part2_total}')


if __name__ == '__main__':
    main()