import sys

with open(sys.argv[1]) as file:
    coord_list = file.read().split('\n')[:-1]
    coord_list = list(map(int, coord_list))
    decryption_key = 811589153
    big_list = [(i, x*decryption_key) for i, x in enumerate(coord_list)]
    coord_list = list(enumerate(coord_list))
    listlen = len(coord_list)

def mix(coord_list):
    for i in range(listlen):
        idx, val = coord_list[i]
        if val == 0:
            continue
        new_idx = (idx + val - 1) % (listlen-1) +1
        
        for c,x in enumerate(coord_list):
            j, v = x
            j = j - (idx < j <= new_idx) + (new_idx <= j < idx)            
            coord_list[c] = (j, v)
        coord_list[i] = (new_idx, val)
    return coord_list

# --- part 1
coord_list = mix(coord_list)

start = [i for i, v in coord_list if v == 0][0]
vals = []
i_list = [(start + 1000) % listlen, (start + 2000) % listlen, (start + 3000) % listlen]
for idx, v in coord_list:
    if idx in i_list:
        vals.append(v)
print("Sum is", sum(vals))

# --- part 2
for i in range(10):
    big_list = mix(big_list)

start = [i for i, v in big_list if v == 0][0]
vals = []
i_list = [(start + 1000) % listlen, (start + 2000) % listlen, (start + 3000) % listlen]
for idx, v in big_list:
    if idx in i_list:
        vals.append(v)
print("Sum is", sum(vals))
