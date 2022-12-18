import sys
from queue import Queue

directions = [(1,0,0), (-1,0,0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1)]
min_val = 10
max_val = 1

with open(sys.argv[1]) as file:
    cube_list = file.read().split('\n')[:-1]
    cubes = [eval(c) for c in cube_list]

exposed_sides = len(cubes) * 6

for idx, cube in enumerate(cubes[:-1]):
    min_val = min(min_val, min(cube))
    max_val = max(max_val, max(cube))
    for c in cubes[idx+1:]:
        zipped = zip(cube, c)
        same_coordinates = sum(a==b for a,b in zip(cube, c))
        is_neighbor = True if sum(abs(a-b) for a,b in zip(cube, c)) == 1 else False
        if same_coordinates == 2 and is_neighbor:
            exposed_sides -= 2
        elif same_coordinates == 3:
            exposed_sides -= 6

print(f"The surface area of the scanned lava droplet is {exposed_sides}.")

min_limit = min_val - 1
max_limit = max_val + 1


def get_neighbors(pos):
    neighbors = []
    for direction in directions:
        neighbor_cube = tuple([a+b for a,b in zip(pos, direction)])
        if max_limit < max(neighbor_cube) or min_limit > min(neighbor_cube):
            continue
        else:
            neighbors.append(neighbor_cube)
    return neighbors

def flood_fill(start_cube):
    water = set()
    if start_cube not in cubes:
        water.add(start_cube)

    queue = [start_cube]
    while queue:
        pos = queue.pop()
        
        for neighbor_cube in get_neighbors(pos):
            if neighbor_cube in water or neighbor_cube in cubes:
                continue
            queue.append(neighbor_cube)
            water.add(neighbor_cube)

    return water

water = flood_fill((min_limit, min_limit, min_limit))
surface = 0
for cube in cubes:
    for neighbor_cube in get_neighbors(cube):
        if neighbor_cube in water:
            # subtract the side of the original cube facing an air pocket neighbor
            surface += 1

print(f"The exterior surface area of the scanned lava droplet is {surface}.")
