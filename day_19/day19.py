import sys
import re
from copy import deepcopy

blueprints = dict()

with open(sys.argv[1]) as file:
    blueprint_list = file.read().split('\n')[:-1]
    for b in blueprint_list:
        matches = list(map(int, re.findall(r'\d+', b)))
        o_r = (matches[3], matches[4], 0, 0)
        g_r = (matches[5], 0, matches[6], 0)
        blueprints[matches[0]] = [(matches[1], 0, 0, 0), (matches[2], 0, 0, 0), o_r, g_r]


def maximize_geodes(step):
    time, robots, ressources, mining = step
    return 1000*mining[3] + 100*mining[2] + 10*mining[1] + mining[0]
    

def build_robots(rob, bp, res):
    to_append = []
    # try to build as many geode robots; therefore reversed order
    for idx in range(len(bp[::-1])-1, -1, -1):
        plan = bp[idx]
        if all(r >= p for r, p in zip(res, plan)):
            new_rob = deepcopy(rob)
            new_rob[idx] += 1
            new_res = [r - p for r,p in zip(res, plan)]
            # we only can build one robot but need all possibilities
            to_append.append((new_rob, new_res))
    appended = len(to_append) > 0
    return appended, to_append


def crack_geodes(bp, time_avail, t):
    geodes_opened = 0
    robots = [1, 0, 0, 0]
    ressources = [0, 0, 0, 0]
    acquired = [0, 0, 0, 0]
    q = [(t, robots, ressources, acquired)]
    max_depth = 1
    while len(q) > 0:
        time, robots, ressources, acquired = q.pop(0)
        if time > max_depth:
            q.sort(key=maximize_geodes, reverse=True)
            q = q[:2000]
            max_depth = time
        if time == time_avail+1:
            geodes_opened = max(geodes_opened, ressources[3])
            continue
        time += 1
        # collect ressources
        new_ressources = [res + rob for res, rob in zip(ressources, robots)]
        acquiring = [m + rob for m, rob in zip(acquired, robots)]
        
        # didn't build robot
        q.append((time, robots, new_ressources, acquiring))

        # build robot
        built, news = build_robots(deepcopy(robots), bp, ressources)
        if built:
            for n_rob, n_res in news:
                new_ressources = [res + rob for res, rob in zip(n_res, robots)]
                q.append((time, n_rob, new_ressources, acquiring))

    return geodes_opened


time_avail = 24
cracked_geodes = [crack_geodes(bp, time_avail, 1) for bp in blueprints.values()]

quality_level = sum(a*b for a,b in zip(cracked_geodes, blueprints.keys()))
print(f"The quality level of all blueprints for {time_avail} minutes is {quality_level}")

time_avail = 32
bp_rest = (blueprints[1], blueprints[2], blueprints[3])
cracked_geodes = [crack_geodes(bp, time_avail, 1) for bp in bp_rest]

opened = 1
for g in cracked_geodes:
    opened *= g
print(f"The quality level of remaining 3 blueprints for {time_avail} minutes is {opened}")
