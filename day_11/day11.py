import sys
from copy import deepcopy
from math import gcd

operation = dict()
test = dict()
action_true = dict()
action_false = dict()

def lcm(*integers):
    it  = iter(integers)
    res = next(it)

    for x in it:
        res = res * x // gcd(res, x)
    return res

### setters
def get_starting_items(line):
    item_list = []
    for l in line[2:]:
        if l[-1:] == ",":
            l = l[:-1]
        item_list.append(int(l))
    return item_list

def set_operation(idx, line):
    operation[idx] = line[11:]

### actions
def inspect_item(item, op):
    # operation is a string
    operands = op.split(" ")
    # operands[3] is symbol
    # operands[4] is number or "old"
    factor = 0
    if operands[4] == "old":
        factor = item
    else:
        factor = int(operands[4])

    if operands[3] == "/":
        item = item / factor
    if operands[3] == "*":
        item = item * factor
    if operands[3] == "-":
        item = item - factor
    if operands[3] == "+":
        item = item + factor
    return item


def test_item(item, div):
    if item % div == 0:
        return True
    return False


with open(sys.argv[1], "r") as file:
    monkey_blocks = file.read().split("\n\n")
    monkey_map = []

    for monkey_index, block in enumerate(monkey_blocks):
        for line in block.split("\n")[1:]:
            if line != '':
                # parse lines
                line = line.strip()
                if "Starting" in line:
                    l = line.split(" ")
                    monkey_map.append(get_starting_items(l))
                if "Operation" in line:
                    set_operation(monkey_index, line)
                if "Test" in line:
                    # test is always a divison
                    l = line.split(" ")
                    test[monkey_index] = int(l[-1])
                if "true" in line:
                    action_true[monkey_index] = int(line[-1])
                if "false" in line:
                    action_false[monkey_index] = int(line[-1])


def play_throwing_game(monkey_map, num_rounds, relief):
    num_inspections = [0 for x in range(len(monkey_blocks))]
    # simplify test through keeping only least common multiple of divisors
    modulus = lcm(*test.values())
    for x in range(num_rounds):
        for monkey_index in range(len(monkey_map)):
            monkey = monkey_map[monkey_index]
            # no starting items
            if len(monkey) < 1:
                continue
    
            for item in monkey:
                # Inspect
                num_inspections[monkey_index] += 1
                worry_level = inspect_item(item, operation[monkey_index])
    
                # Relief through boredom
                worry_level = worry_level // relief
                # only keep smaller worry_levels which preserve divisibility
                worry_level = worry_level % modulus
    
                # Test and Throw
                if test_item(worry_level, test[monkey_index]):
                    monkey_map[action_true[monkey_index]].append(worry_level)
                else:
                    monkey_map[action_false[monkey_index]].append(worry_level)
            
            monkey_map[monkey_index] = []

    return num_inspections

### part 1
num_rounds = 20
num_inspections = play_throwing_game(deepcopy(monkey_map), num_rounds, 3)
max_inspections = sorted(num_inspections)[-2:]
monkey_business = max_inspections[0] * max_inspections[1]
print(f"Level of monkey business after 20 rounds is {monkey_business}")

### part 2
num_rounds = 10000
num_inspections = play_throwing_game(deepcopy(monkey_map), num_rounds, 1)
max_inspections = sorted(num_inspections)[-2:]
monkey_business = max_inspections[0] * max_inspections[1]
print(f"Level of monkey business after 10000 rounds is {monkey_business}")
