import click

def part1(stones_list: list, blinks: int):
    """ Part 1: Use simple array """
    for blink in range(blinks):
        temp_list = list()
        for num in stones_list:
            if num == 0:
                temp_list.append(1)
            elif not len(str(num))%2:
                num1 = num // pow(10, len(str(num))//2)
                num2 = num % pow(10, len(str(num))//2)
                temp_list.extend([num1, num2])
            else:
                temp_list.append(num * 2024)
        # print(f"After {blink} blinks: {temp_list}")
        stones_list = temp_list
    return len(stones_list)

def part2(stones_list: list, blinks: int):
    """ Part 2: Smarter way of storing the stones value """
    def inc_key_val(my_dict: dict, my_key, new_val: int):
        if my_key in my_dict.keys():
            my_dict[my_key] += new_val
        else: 
            my_dict[my_key] = new_val

    stones = dict()
    # Initial round to convert list in dict
    for stone in stones_list:
        inc_key_val(stones, stone, 1)
    
    for blink in range(blinks):
        new_stones = dict()
        for num, count in stones.items():
            if num == 0:
                inc_key_val(new_stones, 1, count)
            elif not len(str(num))%2:
                new_num1 = num // pow(10, len(str(num))//2)
                inc_key_val(new_stones, new_num1, count)

                new_num2 = num % pow(10, len(str(num))//2)
                inc_key_val(new_stones, new_num2, count)
            else:
                new_num = num * 2024
                inc_key_val(new_stones, new_num, count)
        # print(f"After {blink} blinks: {new_stones}")
        stones = new_stones
    
    # Sum all values
    res = 0
    for _, val in stones.items():
        res += val
    return res

@click.command()
@click.option('--file', '-f', help='Input file path.')
def main(file):
    # Read file
    with open(file) as f:
        input = f.read()
    
    stones_list = [int(i) for i in input.strip().split(' ')]
    print(f"Stones {stones_list}")

    blinks = 25
    res = part1(stones_list, blinks)
    print(f'Part 1: Answer is {res}')

    blinks = 75
    res = part2(stones_list, blinks)
    print(f'Part 2: Answer is {res}')

if __name__ == '__main__':
    main()