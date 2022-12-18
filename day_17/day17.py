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
    rocks.append(rock1)
    rocks.append(rock2)
    rocks.append(rock3)
    rocks.append(rock4)
    rocks.append(rock5)
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

def simulate_falling(cave, highest_row, end):
    for rock_count in range(1, end+1):
        rock = rocks.popleft()
        x = 2
        y = len(cave) - len(rock)
        landed = False
        while not landed:
            shift = jets.popleft()
            jets.append(shift)
            if not colliding(x + shift, y, rock, cave, "x"):
                x += shift
            if colliding(x, y-1, rock, cave, "y"):
                landed = True
            else:
                y -= 1
        
        if landed and rock_count == end:
            highest_row = max(highest_row, y + len(rock))
            return highest_row
        if landed and rock_count < end:
            # apply shape to cave
            cave[y:y+len(rock), x:x+len(rock[0])] += rock
            # extend cave hight
            next_rock = rocks.popleft()
            rocks.appendleft(next_rock)
            highest_row = max(highest_row, y + len(rock))
            to_append = highest_row + 3 + len(next_rock) - cave.shape[0]
            if to_append > 0:
                cave = np.vstack((cave, np.zeros((to_append,width), dtype=int)))
            elif to_append < 0:
                cave = cave[:to_append,:]


        rocks.append(rock)
p1 = 2022
cave_height= simulate_falling(cave, 0, p1)
print(cave_height)

p2 = 1000000000000
#cave_height= simulate_falling(cave, 0, p2)
#print(cave_height)
