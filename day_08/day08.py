import sys
import numpy as np

with open(sys.argv[1], "r") as file:
    rows = file.read().splitlines()

row_len = len(rows[0])
col_len = len(rows)

tree_heights = np.zeros((col_len, row_len), dtype=int)

for i in range(col_len):
    heights = rows[i]
    for j in range(row_len):
        tree_heights[i][j] = int(heights[j])

num_edge_trees = 2*(row_len + col_len-2)

def get_visible_inner():
    num_visible = 0
    for i in range(1, col_len-1):
        for j in range(1, row_len-1):
            tree = tree_heights[i][j]
            top_max = np.max(tree_heights[:i,j])
            bottom_max = np.max(tree_heights[i+1:,j])
            left_max = np.max(tree_heights[i,:j])
            right_max = np.max(tree_heights[i,j+1:])
            
            visible = any(tree > x for x in [top_max, bottom_max, left_max, right_max])
            num_visible += 1 if visible else 0
    return num_visible

num_inner_trees = get_visible_inner()
print(f"There are {num_edge_trees + num_inner_trees} visible trees.")

scenic_score_map = np.zeros((col_len, row_len), dtype=int)

def scenic_score(tree, tree_list):
    score = 0
    for t in tree_list:
        if t >= tree:
            score += 1
            break
        score += 1
    return score

def get_scenic_scores():
    num_visible = 0
    for i in range(1, col_len-1):
        for j in range(1, row_len-1):
            tree = tree_heights[i][j]
            scenic_top = scenic_score(tree, tree_heights[:i,j][::-1])
            scenic_bottom = scenic_score(tree, tree_heights[i+1:,j])
            scenic_left = scenic_score(tree, tree_heights[i,:j][::-1])
            scenic_right = scenic_score(tree, tree_heights[i,j+1:])
            
            score = scenic_top * scenic_bottom * scenic_left * scenic_right
            scenic_score_map[i,j] = score
    return np.max(scenic_score_map)

print(f"The ideal spot has a score of {get_scenic_scores()}.")
