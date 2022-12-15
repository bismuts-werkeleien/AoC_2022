import sys
import re

dist = lambda x1,y1,x2,y2 : abs(y2-y1) + abs(x2-x1)

with open(sys.argv[1], "r") as file:
    lines = file.read().split('\n')[:-1]
    positions = [[int(s) for s in re.findall(r'[-]?[\d]+', l)] for l in lines]

dists = [dist(sx, sy, bx, by) for sx, sy, bx, by in positions]

max_grid = max(map(max, positions)) + max(dists) + 10
min_grid = -(abs(min(map(min, positions))) + max(dists) + 10)
# number of positions where beacon cannot be present
num_nos = 0


y = 2000000
#y = 10
# go through grid and see if actual pos is within distance of a signal-beacon pair
for x in range(min_grid, max_grid):
    possible_location = True
    for i, pos in enumerate(positions):
        signal_x, signal_y, beacon_x, beacon_y = pos
        if (x, y) == (beacon_x, beacon_y):
            possible_location = True
            break
        if dist(signal_x, signal_y, x,y) <= dists[i]:
            possible_location = False
            break
    if not possible_location:
        num_nos += 1

print(f"In the row where y={y}, {num_nos} positions cannot contain a beacon.")


distress_range = 4000000
#distress_range = 20
pos_found = False
impossible_beacons = [[] for _ in range(distress_range + 1)]
for i, pos in enumerate(positions):
    signal_x, signal_y, beacon_x, beacon_y = pos
    d = dists[i]
    dy = 0
    while d > 0:
        x_l = max(0, signal_x - d)
        x_r = min(distress_range, signal_x + d)
        if (signal_y >= dy):
            impossible_beacons[signal_y - dy].append([x_l, x_r])
        if (signal_y <= distress_range - dy and dy != 0):
            impossible_beacons[signal_y + dy].append([x_l, x_r])
        dy += 1
        d -= 1

x, y = 0, 0
for y in range(1, distress_range+1):
    row = impossible_beacons[y]
    if not row:
        continue
    
    row.sort()
    if row[0][0] != 0:
        x = 0 
        break
    range_end = row[0][1]        
    for i in range(1, len(row)):
        if range_end >= row[i][0] - 1:
            range_end = max(range_end, row[i][1])
        else:
            break
    if range_end != distress_range:
        x = range_end + 1
        break

print(f"The tuning frequency is {y + 4000000*x}")

