import click
import re

class Machine():
    def __init__(self, part1: bool, buttonA: tuple, buttonB: tuple, prize: tuple):
        self.buttonA = buttonA
        self.buttonB = buttonB
        if part1:
            self.prize = prize
        else:
            self.prize = tuple(map(lambda i, j: i + j, prize, (10000000000000, 10000000000000)))
        self.pressB = self.compute_b_press()
        self.pressA = self.compute_a_press(self.pressB)

    def __str__(self):
        return f"A: {self.buttonA}, B: {self.buttonB}, Prize={self.prize}"
    
    def compute_b_press(self):
        num = self.buttonA[0] * self.prize[1] - self.buttonA[1] * self.prize[0]
        denum = self.buttonA[0] * self.buttonB[1] - self.buttonB[0] * self.buttonA[1]
        return num/denum
    
    def compute_a_press(self, b_press):
        return (self.prize[0] - b_press * self.buttonB[0]) / self.buttonA[0]
    
    def is_solvable(self):
        solvable = False
        if int(self.pressB) == self.pressB and int(self.pressA) == self.pressA:
            solvable = True
        return solvable
    
    def get_token(self):
        return int(3*self.pressA + self.pressB)

@click.command()
@click.option('--file', '-f', help='Input file path.')
def main(file):
    part1 = False

    # Read file
    machines = list()
    with open(file) as f:
        for line in f.read().splitlines():
            if line.startswith('Button A:'):
                buttonA = [int(num) for num in re.findall(r'\d+', line)]
            elif line.startswith('Button B:'):
                buttonB = [int(num) for num in re.findall(r'\d+', line)]
            elif line.startswith('Prize:'):
                prize = [int(num) for num in re.findall(r'\d+', line)]
            else:
                machines.append(Machine(part1, buttonA, buttonB, prize))
        machines.append(Machine(part1, buttonA, buttonB, prize))

    # Compute total token
    res = 0
    for machine in machines:
        if machine.is_solvable():
            res += machine.get_token()

    print(f'Answer is {res}')

if __name__ == '__main__':
    main()