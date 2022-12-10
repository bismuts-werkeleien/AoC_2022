import sys

with open(sys.argv[1], "r") as file:
    lines = file.read().splitlines()
    instructions = [x.split(' ') for x in lines]

def crt_printer(crt):
    line = ''
    for l in crt:
        for c in l:
            line += c
        print(line)
        line = ''

cpu_times = {'noop': 1, 'addx': 2}

reg_x = 1
cycle = 0

signal_strength = [20 + (40*i) for i in range((len(lines)//20))]
s = 0

end_signal = []
crt = [['.' for _ in range(40)] for i in range(6)]
crt_row = -1
window = [-1, 0, 1]
sprite = reg_x
crt_pos = 0

for instruction in instructions:
    for t in range(cpu_times[instruction[0]]):
        if (cycle + t) % 40 == 0:
            crt_row += 1
        sprite = reg_x
        sprite_window = [sprite + i for i in window]
        if crt_pos in sprite_window:
            crt[crt_row][crt_pos] = '#'
        crt_pos = crt_pos + 1 if crt_pos < 39 else 0

    cycle += cpu_times[instruction[0]]
    # check if signal_strength cycle happened in between
    if cycle >= signal_strength[s]:
        end_signal.append(signal_strength[s]*reg_x)
        s += 1

    if instruction[0] == 'addx':
        reg_x += int(instruction[1])


print(sum(end_signal))

crt_printer(crt)
