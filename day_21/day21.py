import sys
from collections import deque
from copy import deepcopy
import math

monkeys = dict()
calculated = dict()

def calc(op, m1, m2):
    if op == "/":
        return m1 / m2
    if op == "*":
        return m1 * m2
    if op == "-":
        return m1 - m2
    if op == "+":
        return m1 + m2

with open(sys.argv[1]) as file:
    yell_list = file.read().split('\n')[:-1]

    for s in yell_list:
        key = s.split(":")[0]
        content = s.split(" ")[1:]
        if len(content) == 1:
            monkeys[key] = int(content[0])
            calculated[key] = int(content[0])
        else:
            monkeys[key] = ((content[0], content[2]), content[1])

def play(monkeys, calculated):
    while len(calculated) < len(monkeys):
        if 'root' in calculated:
            return monkeys['root']
        for monkey in monkeys.keys():
            if not monkey in calculated:
                (m1, m2), op = monkeys[monkey]
                if m1 in calculated and m2 in calculated:
                    res = calc(op, monkeys[m1], monkeys[m2])
                    monkeys[monkey] = res
                    calculated[monkey] = res
                    if monkey == 'root':
                        return math.floor(monkeys['root'])

part1 = play(deepcopy(monkeys), deepcopy(calculated))
print(f"The monkey named root will yell {part1}")

# --- part 2
monkeys['root'] = (monkeys['root'][0], "-")
start, lower = 0, 0
end, upper = 1_000_000_000_000_000, 1_000_000_000_000_000  # for convergence on input
half = (start + end) // 2
monkeys['humn'] = half
switched = False

while (equality := play(deepcopy(monkeys), deepcopy(calculated))) != 0:
    if not switched:
        if equality < 0:
            start = half + 1
        elif equality > 0:
            end = half
    else:
        if equality < 0:
            end = half - 1
        elif equality > 0:
            start = half
    # as we don't know whether an equality check really implies the descent direction as above,
    # try the other way round if it wasn't successful (start and end met)
    if 0 <= end - start <= 1:
        start = lower
        end = upper
        switched = not switched 
    half = (start + end) // 2
    monkeys['humn'] = half

monkeys['humn'] = half

print(f"The monkey named humn has to yell {monkeys['humn']}")
