import sys
from copy import deepcopy
import math
import numpy as np
from collections import deque


with open(sys.argv[1], "r") as file:
    lines = file.read().split('\n')
    width = len(lines) - 1
    topography = np.array([], dtype=int)
    start = (-1,-1)
    end = (-1,-1)
    all_a = []
    for i, l in enumerate(lines[:-1]):
        for j, x in enumerate(l):
            if x == 'S':
                start = (i,j)
                all_a.append(start)
                topography = np.append(topography, [ord('a')])
            elif x == 'E':
                end = (i,j)
                topography = np.append(topography, [ord('z')])
            else:
                if x == 'a':
                    all_a.append((i,j))
                topography = np.append(topography, [ord(x)])
    topography = np.reshape(topography, (width, -1))

neighbor_pos = [(1,0), (-1,0), (0,1), (0,-1)]

def get_valid_neighbors(node, path_tree):
    neighbors = []
    for i,j in neighbor_pos:
        y = i + node[0]
        x = j + node[1]
        if y >= 0 and x >= 0 and y < topography.shape[0] and x < topography.shape[1]:
            height = topography[(y,x)] - topography[node]
            if height <= 1 and (y,x) not in path_tree:
                neighbors.append((y,x))
    return neighbors


num_vertices = len(topography)*len(topography[0])

def visit(start_pos, distance):
    candidates = deque((p, distance) for p in start_pos)
    path_tree = set(start_pos)
    while candidates:
        u, dist = candidates.popleft()

        if u == end:
            print(dist)
            return
        
        neighbors = get_valid_neighbors(u, path_tree)
        for v in neighbors:
            candidates.append((v, dist + 1))
            path_tree.add(v)



visit([start], 0)
visit(all_a, 0)
