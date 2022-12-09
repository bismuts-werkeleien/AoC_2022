import sys

with open(sys.argv[1], "r") as file:
    lines = file.read().splitlines()
    motions = [x.split(' ') for x in lines]

start_pos = (0,0)

part1_visited = {(start_pos)}
part2_visited = {(start_pos)}

moves = {'R': (0,1), 'L': (0,-1), 'U': (1,0), 'D': (-1,0)}

def move_one(pos, direction):
    dy = moves[direction][0]
    dx = moves[direction][1]
    y = pos[0] + dy
    x = pos[1] + dx
    return (y, x)

def sign(x):
    if x > 0:
        return 1
    if x < 0:
        return -1
    return 0

def manage_move(y, x, dist_y, dist_x):
    if dist_y**2 >= 4 or dist_x**2 >= 4:
        y += sign(dist_y)
        x += sign(dist_x)
    return (y, x)
    
rope_len = 9
rope_drag = [start_pos] * (rope_len + 1)

for motion in motions:
    for _ in range(int(motion[1])):
        head_pos = rope_drag[0]
        rope_drag[0] = move_one(head_pos, motion[0])

        for i in range(rope_len):
            pred_y, pred_x = rope_drag[i]
            t_y, t_x = rope_drag[i+1]
            dist_y = pred_y - t_y
            dist_x = pred_x - t_x
            rope_drag[i+1] = manage_move(t_y, t_x, dist_y, dist_x)
        
        part1_visited.add(rope_drag[1])
        part2_visited.add(rope_drag[9])

print(f"1 knot rope tail visited {len(part1_visited)} positions.")
print(f"9 knot rope tail visited {len(part2_visited)} positions.")
