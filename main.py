import objects as obj
import mapTraverse as mapFun
import time
import json
import sys

start_time = time.time()

# Read configurations from file
with open("config.json") as file:
    data = json.load(file)
algo_dic_fun = {'BFS': mapFun.BFS, 'DFS': mapFun.DFS, 'IDDFS': mapFun.IDDFS}
algorithm_name = data["algorithm"]
if algorithm_name not in algo_dic_fun:
    print("Invalid algorithm!")
    sys.exit(1)
max_depth = int(data["max_depth"])
if max_depth < 0:
    print("Invalid max depth!")
    sys.exit(1)
if algorithm_name == 'IDDFS':
    iddfs_step = int(data["iddfs_step"])
    if iddfs_step <= 0:
        print("Invalid IDDFS step!")
        sys.exit(1)
level = 'level_' + data["level"] + '.txt'
# TODO: use parameters

# Read map from file
boxes_init = []
static_map = {}
file = open(level, "r")
y = 0
for line in file:
    x = 0
    for character in line:
        if character == '\n':
            break
        if character == '#':
            static_map[obj.Point(x, y)] = mapFun.Element.Wall
        elif character == '.':
            static_map[obj.Point(x, y)] = mapFun.Element.Goal
        elif character == '$':
            boxes_init.append(obj.Point(x, y))
        elif character == '@':
            player_init = obj.Point(x, y)
        elif character == '*':
            static_map[obj.Point(x, y)] = mapFun.Element.Goal
            boxes_init.append(obj.Point(x, y))
        elif character == '+':
            static_map[obj.Point(x, y)] = mapFun.Element.Goal
            player_init = obj.Point(x, y)
        # elif character == ' ': do nothing
        x += 1
    y += 1

# TODO: Create simple map validation?
#       No 2 player_init, # boxes <= # goals
init_node = obj.Node(player_init, 0, boxes_init)

end_time = time.time()
print(f'Took {end_time - start_time} to read Config and Map')
start_time = end_time

if algorithm_name == 'IDDFS':
    algo = algo_dic_fun[algorithm_name](static_map, init_node, iddfs_step)
else:
    algo = algo_dic_fun[algorithm_name](static_map, init_node)
while not algo.is_algorithm_over():
    curr_node = algo.iterate()
    # print(f'{algo.node_collection}\n')

end_time = time.time()
print(f'Took {end_time - start_time} to run algorithm')

# TODO: Print search params

# TODO: Move printing to function/other place, add return in failure instead of if/else
if not algo.winner_node:
    # Solution not found
    print("Failure!")
else:
    # Solution found
    print("Success!")
    print(f'Depth: {algo.winner_node.depth}; '
          f'Expanded nodes: {algo.expanded_count}; '
          f'Border nodes: {algo.get_border_count()}')
    road_stack = algo.get_winning_road_stack()

    # TODO: Print map instead of nodes
    while road_stack:
        print(f'{road_stack.pop()}\n')
