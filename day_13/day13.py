import sys
from functools import cmp_to_key

with open(sys.argv[1], "r") as file:
    groups = file.read().split('\n\n')
    signals = ['[[2]]', '[[6]]']
    pairs = []
    for g in groups:
        p = g.split("\n")
        pairs.append(p)
        signals.extend(p)
    signals.pop()

idx_list = []

def is_int(s):
    if type(s) is int:
        return True
    return False

def is_ordered(left, right):
    len_l, len_r = len(left), len(right)
    len_max = max(len_l, len_r)
    
    for idx in range(len_max):
        if idx >= len_l:
            return True
        if idx >= len_r:
            return False
        
        l = left[idx]
        r = right[idx]
        
        # both int -> check values
        if is_int(l) and is_int(r):
            if int(l) > int(r):
                return False
            elif int(l) < int(r):
                return True
        else:
            # -> convert to list
            if is_int(r):
                r = [r]
            elif is_int(l):
                l = [l]
            result = is_ordered(l, r)
            if result is not None:
                return result

def sort_signals(signals):
    n = len(signals)
    for i in range(n-1):
        for j in range(0, n-1-i):
            if is_ordered(signals[j+1], signals[j]):
                signals[j], signals[j+1] = signals[j+1], signals[j]
    return signals

for idx, pair in enumerate(pairs):
    left = eval(pair[0])
    right = eval(pair[1])

    if is_ordered(left, right):
        idx_list.append(idx+1)

print(sum(idx_list))

part2 = 1
signals = [eval(x) for x in signals]
sorted_signals = sort_signals(signals)
for idx, signal in enumerate(sorted_signals):
    if signal == [[2]]: part2 *= (idx+1)
    if signal == [[6]]: part2 *= (idx+1)
print(part2)

