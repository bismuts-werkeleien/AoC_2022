import sys
import re
from collections import deque
import numpy as np
from copy import deepcopy


def build_rocks(rocks):
    rock1 = [[1, 1, 1, 1]]
    rock2 = [[0, 1, 0],[1, 1, 1],[0, 1, 0]]
    rock3 = [[1, 1, 1],[0 , 0, 1],[0, 0, 1]]
    rock4 = [[1],[1],[1],[1]]
    rock5 = [[1, 1],[1, 1]]
    rocks.append((0, rock1))
    rocks.append((1, rock2))
    rocks.append((2, rock3))
    rocks.append((3, rock4))
    rocks.append((4, rock5))
    return rocks

def colliding(x, y, rock, cave, direction):
    if direction == "x":
        if x < 0 or x+len(rock[0])>7:
            return True
    elif direction == "y":
        if y < 0:
            return True

    x_range = len(rock[0])
    y_range = len(rock)

    for j in range(y,y+y_range):
        for i in range(x,x+x_range):
            if cave[j,i] == 1 and rock[j-y][i-x] == 1:
                return True
    return False
    
conversion = {"<": -1, ">": 1}

with open(sys.argv[1], "r") as file:
    line = [*file.readline()][:-1]
    jets = deque([])
    for i in [conversion[j] for j in line]:
        jets.append(int(i))

width = 7
cave = np.zeros((4, width), dtype=int)
rocks = build_rocks(deque([]))

def simulate_falling(cave, jets, rocks, highest_row, end):
    jet_idx = 0
    cycle_track = {}
    highest_row = 0

    for rock_count in range(end):
        rock_idx, rock = rocks.popleft()
        x = 2
        y = len(cave) - len(rock)

        if rock_count > 1000:
            key = (rock_idx, jet_idx)
            if key in cycle_track:
                prev_rock_count, prev_row_height = cycle_track[key]
                cycle_len = rock_count - prev_rock_count
                if rock_count % cycle_len == end % cycle_len:
                    print(f"cycle of period {cycle_len} from rocks {prev_rock_count} to {rock_count}")
                    # detected cycle of length of cycle_len
                    #
                    # from now on we will be stuck in a cycle, so we can fast-foward
                    # and calculate the height that added up since entering the cycle.
                    # This times the number of rounds we will cycle from now on gives us
                    # the overall height that will be added to the height we obtained before cycling.
                    batch_height = highest_row - prev_row_height
                    rocks_remaining = end - rock_count
                    cycles_remaining = (rocks_remaining // cycle_len) + 1
                    return prev_row_height + (batch_height * cycles_remaining)
            else:
                cycle_track[key] = (rock_count, highest_row)


        landed = False
        while not landed:
            shift = jets.popleft()
            jets.append(shift)
            jet_idx = (jet_idx + 1) % len(jets)
            if not colliding(x + shift, y, rock, cave, "x"):
                x += shift
            if colliding(x, y-1, rock, cave, "y"):
                landed = True
            else:
                y -= 1
        
        if landed and rock_count == end - 1:
            highest_row = max(highest_row, y + len(rock))
            return highest_row

        if landed and rock_count < end - 1:
            # apply shape to cave
            cave[y:y+len(rock), x:x+len(rock[0])] += rock
            # extend cave hight
            next_idx, next_rock = rocks.popleft()
            rocks.appendleft((next_idx, next_rock))
            highest_row = max(highest_row, y + len(rock))
            to_append = highest_row + 3 + len(next_rock) - (cave.shape[0])
            if to_append > 0:
                cave = np.vstack((cave, np.zeros((to_append,width), dtype=int)))
            elif to_append < 0:
                cave = cave[:to_append,:]


        rocks.append((rock_idx, rock))
p1 = 2022
cave_height= simulate_falling(deepcopy(cave), deepcopy(jets), deepcopy(rocks), 0, p1)
print(cave_height)

p2 = 1000000000000
cave_height= simulate_falling(deepcopy(cave), deepcopy(jets), deepcopy(rocks), 0, p2)
print(cave_height)
