import sys
from collections import deque
from copy import deepcopy

monkeys = dict()
calculated = dict()

def calc(op, m1, m2):
    if op == "/":
        return m1 // m2
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
                        return monkeys['root']

part1 = play(deepcopy(monkeys), deepcopy(calculated))
print(f"The monkey named root will yell {part1}")

# --- part 2
(m1, m2), op = monkeys['root']
monkeys['root'] = ((m1, m2), "-")
start, lower = 0, 0
end, upper = 1_000_000_000_000_000, 1_000_000_000_000_000  # input
#end, upper = 1_000, 1_000  # sufficiently fo test
half = (start + end) // 2
monkeys['humn'] = half

while (equality := play(deepcopy(monkeys), deepcopy(calculated))) != 0:
    if equality < 0:
        start = half
    elif equality > 0:
        end = half - 1 

    if 1 <= end - start <= 2:
        start = upper
        end = lower
    half = (start + end) // 2
    monkeys['humn'] = half

# could be one less due to integer division
monkeys['humn'] = half - 1
if play(deepcopy(monkeys), deepcopy(calculated)) != 0:
    monkeys['humn'] = half

print(f"The monkey named humn has to yell {monkeys['humn']}")
