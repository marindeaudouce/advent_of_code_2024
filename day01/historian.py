import click
import pandas as pd

@click.command()
@click.option('--file', '-f', help='Input file path.')
def part1(file):
    """ Part 1 """
    csvfile = pd.read_csv(file, sep=' ', names=['col1', 'col2'])

    # Sort each list individually
    for col in csvfile:
        csvfile[col] = csvfile[col].sort_values(ignore_index=True)
    
    # Compute the difference 
    csvfile['diff'] = abs(csvfile['col1'] - csvfile['col2'])

    # Compute the sum of the difference
    res = csvfile['diff'].sum()
    print(f'Part 1: Answer is {res}')

@click.command()
@click.option('--file', '-f', help='Input file path.')
def part2(file):
    """ Part 2 """
    csvfile = pd.read_csv(file, sep=' ', names=['col1', 'col2'])

    # Serie containing counts of unique values of list 2
    l2_count = csvfile['col2'].value_counts()

    res = 0
    for elem in csvfile['col1']:
        occurences = l2_count.get(elem) if l2_count.get(elem) != None else 0
        res += elem * occurences
    
    print(f'Part 2: Answer is {res}')

if __name__ == '__main__':
    # part1()
    part2()