import sys
import re

with open(sys.argv[1], "r") as file:
    in_sections = [value for value in file.read().splitlines()]
    sections = []
    for line in in_sections:
        sections.append([int(item) for item in re.split(',|-', line)])

# print(sections)

containment_count = 0
overlap_count = 0
for pair in range(len(sections)):
    i = sections[pair][0]
    j = sections[pair][1]
    k = sections[pair][2]
    l = sections[pair][3]
    # first elf has all section IDs contained in IDs of second elf or vice versa
    if (i >= k and j <= l) or (i <= k and j >= l):
        containment_count += 1
    # overlaps don't have to be fully contained
    if (i <= k and j >= k) or (i <= l and j >= l) or (i >= k and j <= l) or (i <= k and j >= l):
        overlap_count += 1

print(f"Containments: {containment_count} and overlaps: {overlap_count}")
