import sys
import re
from queue import Queue

valve_flows = dict()
valve_tunnels = dict()
dists = dict()

def build_map(line):
    key = line[1]
    flow_rate = [int(n) for n in re.findall(r'\b\d+\b', line[4])][0]
    valves = [l for l in " ".join(line[9:]).split(", ")]
    valve_flows[key] = flow_rate
    valve_tunnels[key] = valves

def get_distances(tunnels, flows, start):
    q = Queue()
    dist = dict()
    visited = {start}
    q.put(start)
    while not q.qsize() < 1:
        valve = q.get()
        if valve == start:
            dist[valve] = 0
        for v in tunnels[valve]:
            if v not in visited:
                if not v in dist:
                    dist[v] = dist[valve] + 1
                elif dist[v] > dist[valve] + 1:
                    dist[v] = dist[valve] + 1
                q.put(v)
                visited.update({v})
    remove = []
    for k,v in dist.items():
        if flows[k] <= 0 or v <= 0:
            remove.append(k)
    for valve in remove:
        dist.pop(valve)
    return dist



with open(sys.argv[1], "r") as file:
    lines = file.read().split('\n')[:-1]
    p = [line.split(" ") for line in lines]
    for l in p:
        build_map(l)
    for k, v in valve_tunnels.items():
        dists[k] = get_distances(valve_tunnels, valve_flows, k)
    remove = []
    for valve,flow in valve_flows.items():
        if flow <= 0 and valve != "AA":
            remove.append(valve)
    for valve in remove:
        dists.pop(valve)


released_pressure = 0
def dfs(pressure, curr_pos, opened, overall_time, time, elephant):
    global released_pressure
    released_pressure = max(released_pressure, pressure)
    for valve, d in dists[curr_pos].items():
        if valve not in opened and time + d < overall_time:
            flow = valve_flows[valve]
            dfs(pressure + flow*(overall_time-time-d), valve, opened | set([valve]), overall_time, 1+time+d, elephant)
    if elephant == True:
        dfs(pressure, "AA", opened, 25, 0, False)

dfs(0, "AA", set(), 29, 0, False)
print(f"We can release {released_pressure} pressure")

# there is an elephant in the room...
released_pressure = 0
dfs(0, "AA", set(), 25, 0, True)
print(f"With help of the elephant, we can release {released_pressure} pressure")


