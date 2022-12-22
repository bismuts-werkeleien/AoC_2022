import sys
from collections import deque
from copy import deepcopy
import re

map_coordinates = []
start = None
facing = 'E'
directions = {'E': (0, 1), 'S': (1, 0), 'W': (0, -1), 'N': (-1, 0)}
opposite_dirs = {'E': (0, -1), 'S': (-1, 0), 'W': (0, 1), 'N': (1, 0)}
turns = {('E','R'): 'S', ('E', 'L'): 'N', ('S','R'): 'W', ('S', 'L'): 'E', ('W','R'): 'N', ('W', 'L'): 'S', ('N','R'): 'E', ('N', 'L'): 'W'}
conversion = {'E': 0, 'S': 1, 'W': 2, 'N': 3}

def cube_wrap(pos, facing, map_coordinates):
    # the current pos has to be on an edge since the next step in facing direction already saw abyss
    edge = None
    offset = 0
    # find edge by coords
    for key, e in edge_coords.items():
        c1, c2 = e[0], e[1]
        if (key, facing) in neighbor_edges and c1[0] <= pos[0] <= c2 [0] and c1[1] <= pos[1] <= c2[1]:
            edge = key
            offset = max(pos[0]-c1[0], pos[1]-c1[1])
            break
    # determine correct new edge and new facing. There is only one possible new facing for a new edge
    if (edge, facing) in neighbor_edges:
        new_edge, new_facing = neighbor_edges[(edge, facing)]
        # determine new pos on that edge
        c1, c2 = edge_coords[new_edge]
        npy, npx = c1[0], c1[1]
        if c1[0] - c2[0] == 0:
            # add offset to col
            if edge in same_coord_edges:
                npx = c1[1] + offset
            else:
                npx = c2[1] - offset
        else:
            # add offset to row 
            if edge in same_coord_edges:
                npy = c1[0] + offset
            else:
                npy = c2[0] - offset
        new_pos = (npy, npx)

        return new_pos, new_facing
    return None


def wrap(pos, facing, map_coordinates):
    prev_pos, next_pos = pos, pos
    while map_coordinates[next_pos[0]][next_pos[1]] != ' ':
        prev_pos = next_pos
        npy, npx = (np+d for np, d in zip(next_pos,opposite_dirs[facing]))
        next_pos = (npy, npx)
    return prev_pos


def move_forward(pos, facing, map_coordinates, p2):
    cont = True
    py, px = (p+d for p, d in zip(pos,directions[facing]))
    if map_coordinates[py][px] == '.':
        return True, (py, px), facing
    if map_coordinates[py][px] == '#':
        return False, pos, facing
    else:
        py, px, new_facing = None, None, facing
        # wrap o the other side for this facing direction
        if not p2:
            py, px = wrap(pos, facing, map_coordinates)
        else:
            # do cube magic
            (py, px), new_facing = cube_wrap(pos, facing, map_coordinates)
        # if we hit a wall there, don't continue and stay where we are
        if map_coordinates[py][px] == '#':
            return False, pos, facing
        return True, (py, px), new_facing


with open(sys.argv[1]) as file:
    input_list = file.read().split('\n\n')
    instruction_list = input_list[-1]
    instruction_list = re.findall(r"[^\W\d_]+|\d+", instruction_list)
    instruction_list = list(map(lambda x: x if not x.isdigit() else int(x), instruction_list))
    instruction_list = instruction_list[::-1]

    rows = input_list[0].split('\n')
    #TODO white-space padding
    for i, row in enumerate(rows):
        map_coordinates.append([])
        for j, c in enumerate(row):
            map_coordinates[i].append(c)
            if start is None and c != " ":
                start = (i, j)

def get_pwd(instruction_list, facing, start, p2: False):
    pos = start
    while instruction_list:
        instruction = instruction_list.pop()
        if type(instruction) == int:
            for i in range(instruction):
                cont, pos, facing = move_forward(pos, facing, map_coordinates, p2)
                if not cont:
                    break
        else:
            facing = turns[(facing, instruction)]
    
    password = conversion[facing] + 1000*(pos[0]) + 4*(pos[1])
    return password

print(f"The final password on a 2D map is {get_pwd(deepcopy(instruction_list), 'E', start, False)}.\n")

# --- part 2
neighbor_edges = {('a', 'N'): ('l', 'E'), ('b', 'N'): ('n', 'N'), ('c', 'W'): ('i', 'E'), ('d', 'E'): ('j', 'W'), ('e', 'S'): ('g', 'W'), ('f', 'W'): ('h', 'S'), ('g', 'E'): ('e', 'N'), ('h', 'N'): ('f', 'E'), ('i', 'W'): ('c', 'E'), ('j', 'E'): ('d', 'W'), ('k', 'S'): ('m', 'W'), ('l', 'W'): ('a', 'S'), ('m', 'E'): ('k', 'N'), ('n', 'S'): ('b', 'S')}
test_neighbor_edges = {('a', 'N'): ('d', 'S'), ('b', 'W'): ('e', 'S'), ('c', 'E'): ('l', 'W'), ('d', 'N'): ('a', 'S'), ('e', 'N'): ('b', 'E'), ('f', 'W'): ('n', 'N'), ('g', 'E'): ('j', 'S'), ('h', 'S'): ('m', 'N'), ('i', 'S'): ('k', 'E'), ('j', 'N'): ('g', 'W'), ('k', 'W'): ('i', 'N'), ('l', 'E'): ('c', 'W'), ('m', 'S'): ('h', 'N'), ('n', 'S'): ('f', 'E')}


edge_coords = {'a': [(1,51), (1,100)], 'b': [(1,101), (1,150)], 'c': [(1,51), (50,51)], 'd': [(1,150), (50,150)], 'e': [(50,101), (50,150)], 'f': [(51,51), (100,51)], 'g': [(51,100), (100,100)], 'h': [(101,1), (101,50)], 'i': [(101,1), (150,1)], 'j': [(101,100), (150,100)], 'k': [(150,51), (150,100)], 'l': [(151,1), (200,1)], 'm': [(151,50), (200,50)], 'n': [(200,1), (200,50)]}

test_edge_coords = {'a': [(1,9), (1,12)], 'b': [(1,9), (4,9)], 'c': [(1,12), (4,12)], 'd': [(5,1), (5,4)], 'e': [(5,5), (5,8)], 'f': [(5,1), (8,1)], 'g': [(5,12), (8,12)], 'h': [(8,1), (8,4)], 'i': [(8,5), (8, 8)], 'j': [(9,13), (9,16)], 'k': [(9,9), (12, 9)], 'l': [(9, 16), (12, 16)], 'm': [(12,9), (12,12)], 'n': [(12,13), (12,16)]}

same_coord_edges = ['a', 'b', 'e', 'f', 'g', 'h', 'k', 'l', 'm', 'n']
test_same_coord_edges = ['b', 'e']

print(f"The final password on a cube is {get_pwd(deepcopy(instruction_list), 'E', start, True)}.")
