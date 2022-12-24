import sys

directions = {'v': (1,0), '^': (-1,0), '>': (0, 1), '<': (0, -1), '.': (0,0)}
elves_start = (0,0)
elves_end = (0,0)
blizzards = dict()  # pos: dir
walls = set()

with open(sys.argv[1]) as file:
    start_list = file.read().split('\n')[:-1]
    # These indices shifts look illegal but required less brain
    # on the modulus operation for the blizzard wrap around/respawn.
    for y, row in enumerate(start_list):
        for x, e in enumerate(row):
            if y == 0 and e != '#':
                elves_start = (y-1, x-1)
            elif y == len(start_list) - 1 and e != '#':
                elves_end = (y-1, x-1)
            elif e == ">" or e == "<" or e == "^" or e == "v":
                blizzards[(y-1,x-1)] = directions[e]
            elif e == '#':
                walls.add((y-1,x-1))

walls |= {(-2, x) for x in range(elves_start[1]-1, elves_start[1]+2)}
borders = (max(y for y,x in walls), max(x for y,x in walls))

time = 0
elves_pos = {elves_start}
destinations = [elves_end, elves_start, elves_end]
while destinations:
    time += 1
    # Wanted to store a blizzards position, direction and start first but turns out
    # calculating a new set with the new positions each time is much faster than
    # actually moving the blizzard positions in a new dict one step each time which took forever.
    new_blizzards = {((pos[0] + time*d[0])%borders[0], (pos[1] + time*d[1])%borders[1]) for pos, d in blizzards.items()}
    next_elves = {(pos[0] + d[0], pos[1] + d[1]) for d in directions.values() for pos in elves_pos}
    
    # Don't let elves move to places with blizzards or walls
    occupied = new_blizzards | walls
    elves_pos = next_elves - occupied
    if destinations[-1] in elves_pos:
        if len(destinations) == 3:
            print(f"It takes at least {time} minutes to reach the exit")
        # set new starting point and go back through blizzard field
        elves_pos = {destinations.pop()}


print(f"It takes at least {time} minutes to reach exit, start and exit again.")
