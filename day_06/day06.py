import sys
from copy import deepcopy

with open(sys.argv[1], "r") as file:
    signal = file.readline()

# marker has to appear in one row
def get_start(signal, marker_length):
    marker = ""
    for idx, c in enumerate(signal):
        if len(marker) == marker_length:
            print(f"The marker received is {marker}")
            return idx
        if c in marker:
            # reset marker until duplicate character
            marker = marker[marker.find(c)+1:]
            marker += c
        elif len(marker) < marker_length:
            marker += c

packet_start = get_start(signal, 4)
print(f"Sequence starts after character {packet_start}")

message_start = get_start(signal, 14)
print(f"Sequence starts after character {message_start}")
