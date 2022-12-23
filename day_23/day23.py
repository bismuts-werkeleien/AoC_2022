import sys
from collections import deque
from copy import deepcopy

directions = {'S': (1,0), 'N': (-1,0), 'E': (0, 1), 'W': (0, -1), 'SE': (1, 1), 'SW': (1, -1), 'NW': (-1, -1), 'NE': (-1, 1)}
elves_pos = set()
consider = deque([('N', 'NE', 'NW'), ('S', 'SE', 'SW'), ('W', 'NW', 'SW'), ('E', 'NE', 'SE')])

with open(sys.argv[1]) as file:
    start_list = file.read().split('\n')[:-1]
    for y, row in enumerate(start_list):
        for x, e in enumerate(row):
            if e == '#':
                elves_pos.add((y, x))

def look_around(pos, con, con1, con2, elves_pos):
    d = tuple(p+c for p, c in zip(pos, directions[con]))
    d1 = tuple(p+c for p, c in zip(pos, directions[con1]))
    d2 = tuple(p+c for p, c in zip(pos, directions[con2]))

    if not (d2 in elves_pos or d1 in elves_pos or d in elves_pos):
        return d
    return None

def game_of_elves(generations, elves_pos, dir_prio):
    for r in range(generations):
        proposed_moves = dict()
    
        # calc next pos
        need_moves = False
        for pos in elves_pos:
            num_moves = 0
            new_direction = None
            for (d, d1, d2) in reversed(dir_prio):
                if not (nd := look_around(pos, d, d1, d2, elves_pos)) is None:
                    num_moves += 1
                    new_direction = nd
                    
            if num_moves == 4:
                # we don't need to move
                proposed_moves[pos] = [pos]
            elif num_moves == 0:
                # neighbors everywhere
                need_moves = True
                proposed_moves[pos] = [pos]
            else:
                need_moves = True
                if new_direction in proposed_moves:
                    proposed_moves[new_direction].append(pos)
                else:
                    proposed_moves[new_direction] = [pos]
    
        if not need_moves:
            return r, elves_pos
    
        #maybe step to next pos
        new_elf_pos = set()
        for new_pos, elves in proposed_moves.items():
            if len(elves) > 1:
                # rollback
                new_elf_pos.update(elves)
    
            else:
                new_elf_pos.add(new_pos)
        elves_pos = new_elf_pos
        
        # rotate directions to consider
        dir_prio.rotate(-1)
    return generations, elves_pos

# --- part 1
# count number of ground tiles
_, elves = game_of_elves(10, deepcopy(elves_pos), deepcopy(consider))
min_y, min_x = tuple(map(min, zip(*elves)))
max_y, max_x = tuple(map(max, zip(*elves)))
# number of ground points = area of ractangle - number of contained elves
area = (max_y - min_y + 1)*(max_x - min_x + 1)
ground = area - len(elves_pos)
print(f"There are {ground} empty ground tiles.")

# --- part 2
# count number of ground tiles
p2_r, elves = game_of_elves(2000, deepcopy(elves_pos), deepcopy(consider))
print(f"Finished in round {p2_r+1}")
