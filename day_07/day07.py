import sys
from copy import deepcopy

class Dir_Tree(object):
    def __init__(self):
        self.name = None
        self.children = None
        self.parent = None
        self.type = None
        self.size = 0

    def create_root(self, name):
        self.name = name
        self.type = "dir"
        self.children = []
        return self

    def update_size(self, size):
        self.size += size
        if self.parent is not None:
            self.parent.update_size(size)

    def insert(self, node, name, filetype, size):
        self.children.append(node)
        node.name = name
        node.type = filetype
        node.size = size
        node.parent = self
        if filetype == "dir":
            node.children = []
        else:
            self.update_size(size)

with open(sys.argv[1], "r") as file:
    output = file.read().split("$")
    terminal_output = []
    # get rid of leading empty line
    output = output[1:]
    for line in output:
        elements = line.split("\n")
        # remove trailing whitespace
        elements = elements[:-1]
        for idx, e in enumerate(elements):
            elements[idx] = e.strip()
        terminal_output.append(elements)

def build_dir_structure(terminal_output):
    current_node = None
    root = Dir_Tree()
    root.create_root("/")
    for line in terminal_output:
        statement = line[0].split(" ")
        if statement[0] == "cd":
            # cd /
            if statement[1] == "/":
                current_node = root            
            # cd ..
            elif statement[1] == "..":
                if current_node.parent is None:
                    current_node = root
                else:
                    current_node = current_node.parent
            # cd dir
            else:
                if statement[1] not in current_node.children:
                    node = Dir_Tree()
                    current_node.insert(node, statement[1], "dir", 0)
                    current_node = node
                else:
                    current_node = node
        elif statement[0] == "ls":
            listings = line[1:]
            for listing in listings:
                l = listing.split(" ")
                if l[0] == "dir" and l[1] not in current_node.children:
                    node = Dir_Tree()
                    current_node.insert(node, l[1], "dir", 0)
                else:
                    node = Dir_Tree()
                    current_node.insert(node, l[1], "file", int(l[0]))

    return root
                    
def get_small_dir_sum(node, size_sum):
    if node.type == "dir":
        if node.size <= 100000:
            size_sum += node.size
        for child in node.children:
            size_sum = get_small_dir_sum(child, size_sum)
    return size_sum


root = build_dir_structure(terminal_output)
actual_size = root.size
print(f"Sum of total sizes of the small directories: {get_small_dir_sum(root, 0)}")

# ---- part 2 ----
AVAILABLE_SIZE = 70000000
UNUSED_SPACE_NEEDED = 30000000
space_to_delete = UNUSED_SPACE_NEEDED - (AVAILABLE_SIZE - actual_size)

def get_dir_candidate(node, size_freed):
    if node.type == "dir":
        if node.size >= space_to_delete:
            size_freed = node.size if node.size < size_freed else size_freed
        for child in node.children:
            size_freed = get_dir_candidate(child, size_freed)
    return size_freed

print(f"Size to free by one dir: {get_dir_candidate(root, root.size)}")




