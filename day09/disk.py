import click

def compute_result(map: dict):
    res = 0
    for key, values in map.items():
        for val in values:
            res += key * val
    return res

def part1(map: dict, empty_pos: list):
    """ Part 1 """
    new_map = dict()
    new_empty = empty_pos
    for id in reversed(map.keys()):
        positions = map.get(id)
        pos_nbr = len(positions)

        all_positions = positions + new_empty
        all_positions.sort()
        positions = all_positions[:pos_nbr]
        new_empty = all_positions[pos_nbr:]
        
        new_map[id] = positions
    return new_map

def part2(map: dict, empty_pos: list):
    """ Part 2 """
    def groupc(data):
        result = []
        i = 0
        while i < len(data):
            j = i
            while j < len(data) - 1 and data[j + 1] == data[j] + 1:
                j += 1
            result.append(list(range(data[i], data[j] + 1, 1)))
            i = j + 1
        return result
    
    new_map = dict()
    new_empty = empty_pos
    for id in reversed(map.keys()):
        positions = map.get(id)
        pos_nbr = len(positions)

        group_empty = list(groupc(new_empty))
        new_grp = []
        for grp in group_empty:
            if pos_nbr <= len(grp):
                all_positions = positions + grp
                all_positions.sort()
                positions = all_positions[:pos_nbr]
                new_grp = all_positions[pos_nbr:]
                break
        new_empty = list(set(new_empty) - set(grp))
        new_empty.extend(new_grp)
        new_empty.sort()
        new_map[id] = positions

    return new_map

@click.command()
@click.option('--file', '-f', help='Input file path.')
def main(file):
    # Read file
    with open(file) as f:
        input = f.read()

    disk_map = dict()
    empty_pos = list()
    pos = 0
    for idx, val in enumerate(input):
        if idx%2:
            # empty positions index
            empty_pos.extend([pos + i for i in range(int(val))])
        else:
            # ID: list(all positions)
            disk_map[idx//2] = [pos + i for i in range(int(val))]
        pos += int(val)

    new_map = part1(disk_map, empty_pos)
    res = compute_result(new_map)
    print(f'Part 1: Answer is {res}')

    new_map = part2(disk_map, empty_pos) # ultra long
    res = compute_result(new_map)
    print(f'Part 2: Answer is {res}')

if __name__ == '__main__':
    main()