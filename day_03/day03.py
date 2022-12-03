import sys

with open(sys.argv[1], "r") as file:
    rucksacks = [value for value in file.read().splitlines()]

rucksack_halves = []
for i in range(len(rucksacks)):
    half = len(rucksacks[i])//2
    rucksack_halves.append(rucksacks[i][0:half])
    rucksack_halves.append(rucksacks[i][half:])

# determine duplicates, claculate their priority and remember rucksack_halves index
duplicates = set()
for i in range(0, len(rucksack_halves), 2):
    for j in rucksack_halves[i]:
        if j in rucksack_halves[i+1]:
            priority =  ord(j)-96 if j.islower() else ord(j)-38
            duplicates.add((j, priority, i))

duplicate_sum = 0
for item, prio, idx in duplicates:
    duplicate_sum += prio
print(f"Summed up duplicates: {duplicate_sum}")

# --- part 2 ---

badges = set()
for i in range(0, len(rucksacks), 3):
    for j in rucksacks[i]:
        if j in rucksacks[i+1] and j in rucksacks[i+2]:
            priority =  ord(j)-96 if j.islower() else ord(j)-38
            badges.add((j, priority, i))

badges_sum = 0
for item, prio, idx in badges:
    badges_sum += prio
print(f"Summed up badges: {badges_sum}")
