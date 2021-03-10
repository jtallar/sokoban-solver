import objects as obj
import mapTraverse as mapFun
import time
import json

start_time = time.time()

# Read configurations from file
with open("config.json") as file:
    data = json.load(file)
algorithm = data["algorithm"]
depth = data["depth"]
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
            continue
        x += 1
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
        elif character == ' ':
            continue
    y += 1

# TODO: Create simple map validation?
#       No 2 player_init, # boxes <= # goals
init_node = obj.Node(player_init, 0, boxes_init)

end_time = time.time()

# Print search params
print('---------------------------------------- \nSearch parameters', '\n\tAlgorithm:\t', algorithm)
print('\tMax. Depth:\t', depth, '\n----------------------------------------')

print(f'Loading Configuration & Level Map \t 🕓 {end_time - start_time} seconds')
start_time = end_time

algo = mapFun.BFS(static_map, init_node)
while not algo.is_algorithm_over():
    curr_node = algo.iterate()
    # print(f'{algo.node_collection}\n')

end_time = time.time()
print(f'Algorithm Run Completed \t\t 🕓 {end_time - start_time} seconds\n----------------------------------------\n')

# TODO: Move printing to function/other place, add return in failure instead of if/else
if not algo.winner_node:
    # Solution not found
    print("Failure! No solution has been found.")
else:
    # Solution found
    print("\t\t   🎉  Winner!  🎉 ")
    print(f'\nDepth: {algo.winner_node.depth}\t '
          f'Expanded nodes: {algo.expanded_count}\t '
          f'Border nodes: {algo.get_border_count()}\n')
          # TODO --> costo de la solucion?
    road_stack = algo.get_winning_road_stack()

    # TODO: Print map instead of nodes
    while road_stack:
        print(f'{road_stack.pop()}\n')
