import sys

with open(sys.argv[1], "r") as file:
    lines = file.read().split('\n')[:-1]
    p = [line.split(" -> ") for line in lines]
    paths = [[eval(z) for z in l] for l in p]


sand_start = (500,0)

def build_rocks(p1, p2):
    d_x = p1[0] - p2[0]
    d_y = p1[1] - p2[1]
    rock_line = []
    rock_dict = dict()
    if d_x > 0:
        rock_line.extend([(p1[0]-x,p1[1]) for x in range(d_x)])
    elif d_x < 0:
        rock_line.extend([(p1[0]+x,p1[1]) for x in range(abs(d_x))])
    if d_y > 0:
        rock_line.extend([(p1[0],p1[1]-y) for y in range(d_y)])
    elif d_y < 0:
        rock_line.extend([(p1[0],p1[1]+y) for y in range(abs(d_y))])
    rock_line.append(p2)
    for key in rock_line:
        rock_dict[key] = '#'
    return rock_dict

# build rock lines
rocks = dict()
for path in paths:
    # get pairwise rock lines
    for idx, p1 in enumerate(path[:-1]):
        rocks.update(build_rocks(p1, path[idx+1]))

# pour sand
x_min, y_min = map(min, zip(*rocks.keys()))
x_max, y_max = map(max, zip(*rocks.keys()))

def can_land(x, y):
    return x_min < x < x_max and y < y_max

def get_next_positions(x, y, cave):
    # always fall one down and maybe one to left/right
    for dx in [0,-1, 1]:
        candidate = (x + dx, y + 1)
        # don't go to the right if left already falls through
        if candidate not in cave and candidate[1] <= y_max:
            return candidate

def pour_sand(cave, sand_start, part):
    sand = sand_start
    while True:
        if sand_start in cave:
            break
        if part == 1 and not can_land(*sand):
            break
        if part == 2 and not can_land(*sand):
            # apply sand to cave
            cave[sand] = 'o'
            sand = sand_start
            continue

        # get  next falling sand
        possible_space = get_next_positions(*sand, cave)
        #print(possible_space)
        if not possible_space is None:
            sand = possible_space
            continue
        # apply sand to cave
        cave[sand] = 'o'
        sand = sand_start
    
    return cave


cave = rocks
cave = pour_sand(cave, sand_start, 1)
landed_sand = sum([1 for v in cave.values() if v == 'o'])
print(landed_sand)

# no idea why it's +1 and not +2 but right now I couldn't care less
y_max += 1 
x_min = -sys.maxsize
x_max = sys.maxsize 
cave = pour_sand(cave, sand_start, 2)
landed_sand = sum([1 for v in cave.values() if v == 'o'])
print(landed_sand)
