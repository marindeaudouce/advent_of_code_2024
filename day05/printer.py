import click

def check_valid_order(rules, update):
    is_valid = True
    for idx in range(len(update) - 1):
        if update[idx + 1] in rules.keys():
            if update[idx] in rules.get(update[idx + 1]):
                is_valid = False
                break
    return is_valid

def reorder(rules, update):
    """ /!\ Affects the value of 'update' param """
    swap = False
    for idx in range(len(update) - 1):
        if update[idx + 1] in rules.keys():
            if update[idx] in rules.get(update[idx + 1]):
                swap = True
                update[idx], update[idx + 1] = update[idx + 1], update[idx]
    return swap

def part1(rules, updates):
    """ Part 1 """
    res = 0
    for update in updates:
        if check_valid_order(rules, update):
            idx = len(update) // 2
            res += update[idx]
                
    print(f'Part 1: Answer is {res}')

def part2(rules, updates):
    """ Part 2 """
    res = 0
    for update in updates:
        if not check_valid_order(rules, update):
            while reorder(rules, update): # Maybe infite, oups
                reorder(rules, update)
            idx = len(update) // 2
            res += update[idx]

    print(f'Part 2: Answer is {res}')

@click.command()
@click.option('--file', '-f', help='Input file path.')
def main(file):
    # Extract useful info from input
    is_rules = True
    rules = dict() # {page number: [list of smaller pages]}
    updates = []
    with open(file) as f:
        for line in f.read().splitlines():
            if line == '':
                is_rules = False # we start reading the updates
            else:
                if is_rules:
                    rule = [int(page) for page in line.split('|')]
                    if rule[0] in rules.keys(): 
                        # if page number already present, append smaller pages list
                        smaller_page = rules.get(rule[0])
                        smaller_page.append(rule[1])
                        rules[rule[0]] = smaller_page
                    else:  
                        rules[rule[0]] = [rule[1]]
                else:
                    updates.append([int(page) for page in line.split(',')])

    part1(rules, updates)
    part2(rules, updates)

if __name__ == '__main__':
    main()