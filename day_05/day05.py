import sys
from copy import deepcopy

def get_layout(layout: str):
    stacks = []
    for line in layout.split("\n")[:-1]:
        # determine index for stack, one stack shift equals 4 whitespaces or [.] plus whitespace
        for stack, pos in enumerate(range(0, len(line), 4)):
            if len(stacks) <= stack:
                # create space holder for to-be-filled-stacks at wrong index
                stacks.append([])
            if line[pos] != " ":
                # actually fill the stack
                stacks[stack].append(line[pos+1])
    for stack in stacks:
        stack.reverse()
    return stacks


def get_moves(procedure: str):
    moves = []
    for line in procedure.split("\n"):
        move = line.split(" ")
        # as we want to have 0-based indices, subtract 1
        moves.append([int(move[1]), int(move[3])-1, int(move[5])-1])
    return moves

with open(sys.argv[1], "r") as file:
    # separate stack layout from procedure
    situation = file.read().split("\n\n")
    stacks = get_layout(situation[0])
    moves = get_moves(situation[1].strip())

def part1(stacks):
    for move in moves:
        amount = move[0]
        source_stack = move[1]
        dest_stack = move[2]
        
        for _ in range(amount):
            stacks[dest_stack].append(stacks[source_stack].pop())
    
    relevant_crates = ""
    for i in range(len(stacks)):
        relevant_crates += stacks[i][-1]
    
    print(f"crates to consider for CrateMover 9000: {relevant_crates}")

def part2(stacks):
    for move in moves:
        amount = move[0]
        source_stack = move[1]
        dest_stack = move[2]
        
        crate_buffer = []
        for _ in range(amount):
            crate_buffer.append(stacks[source_stack].pop())
        crate_buffer.reverse()
        for crate in crate_buffer:
            stacks[dest_stack].append(crate)
    
    relevant_crates = ""
    for i in range(len(stacks)):
        relevant_crates += stacks[i][-1]
    
    print(f"crates to consider for CrateMover 9001: {relevant_crates}")

part1(deepcopy(stacks))
part2(deepcopy(stacks))
