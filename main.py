import objects as obj
import mapTraverse as mapFun
import time
import json
import sys

def printMap(node):
    line = '\t     '
    for iy in range(maxY):
        for ix in range(maxX):
            if(obj.Point(ix, iy) in static_map):                # el punto es Wall o Goal
                if(obj.Point(ix, iy) in node.boxes):            # y tambien es Box
                    line += mapFun.Element.BoxInGoal.value
                elif(obj.Point(ix,iy) == node.player_point):          # o y tambien es Player
                    line += mapFun.Element.PlayerInGoal.value
                elif(static_map[obj.Point(ix, iy)] == mapFun.Element.Wall):    # entonces es Wall?
                    line += mapFun.Element.Wall.value
                else: line += mapFun.Element.Goal.value         # bueno entonces es Goal
            elif obj.Point(ix,iy) == node.player_point:               # no es Wall ni Goal pero es Player
                line += mapFun.Element.Player.value
            elif obj.Point(ix,iy) in node.boxes:                # no es Wall ni Goal ni Plater -> es Box?
                line += mapFun.Element.Box.value            
            else: line += mapFun.Element.Space.value            # entonces no hay nada

        print(line)
        line = '\t     '
    print('\n')

#TODO: Close files

start_time = time.time()

# Read configurations from file
with open("config.json") as file:
    data = json.load(file)
algo_dic_fun = {'BFS': mapFun.BFS, 'DFS': mapFun.DFS, 'IDDFS': mapFun.IDDFS, 
                'GGS': mapFun.GGS}
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
level = data["level"]
print_boolean = data["print"]
if print:
    print_time = float(data["print_time"])
    if print_time < 0:
        print("Invalid printing time!")
        sys.exit(1)

# Read map from file
boxes_init = []
static_map = {}
player_init = None
goal_count = 0
maxY = 0
maxX = 0
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
            goal_count += 1
        elif character == '$':
            boxes_init.append(obj.Point(x, y))
        elif character == '@':
            if player_init:
                print("Invalid map! Cannot have more than one initial player position.")
                sys.exit(1)
            player_init = obj.Point(x, y)
        elif character == '*':
            static_map[obj.Point(x, y)] = mapFun.Element.Goal
            goal_count += 1
            boxes_init.append(obj.Point(x, y))
        elif character == '+':
            if player_init:
                print("Invalid map! Cannot have more than one initial player position.")
                sys.exit(1)
            static_map[obj.Point(x, y)] = mapFun.Element.Goal
            goal_count += 1
            player_init = obj.Point(x, y)
        # elif character == ' ': do nothing
        x += 1
    if x > maxX: maxX = x
    y += 1
maxY = y

if goal_count != len(boxes_init):
    print("Invalid map! Cannot have more goals than boxes.")
    sys.exit(1)

init_node = obj.Node(player_init, 0, boxes_init)

end_time = time.time()

# Print search params
print('---------------------------------------- \nSearch parameters', '\n\tAlgorithm:\t', algorithm_name)
if algorithm_name == 'IDDFS':
    print('\tIDDFS step:\t', iddfs_step)
print('\tMax. Depth:\t', max_depth, '\n\tLevel:\t\t', level)
print('----------------------------------------')

print(f'Load Configuration & Level Map \t\t ⏱  {round(end_time - start_time, 6)} seconds')
start_time = end_time

# TODO: delete this method
def heuristic(node):
    return node.depth

if algorithm_name == 'IDDFS':
    algo = algo_dic_fun[algorithm_name](static_map, init_node, max_depth, iddfs_step)
elif algorithm_name == 'GGS':
    # TODO: Get heuristic function from file + config param
    algo = algo_dic_fun[algorithm_name](static_map, init_node, max_depth, heuristic)
else:
    algo = algo_dic_fun[algorithm_name](static_map, init_node, max_depth)
while not algo.is_algorithm_over():
    curr_node = algo.iterate()
    # print(f'{algo.node_collection}\n')

end_time = time.time()
print(f'Algorithm Run Completed \t\t ⏱  {round(end_time - start_time, 6)} seconds\n----------------------------------------\n')

if not algo.winner_node:
    # Solution not found
    print("\t❌  Failure! No solution found with those params. ❌ ")
    # TODO: Ver si hay que imprimir esta info en caso de falla.
    print(f'Expanded nodes: {algo.expanded_count}\t '
          f'Border nodes: {algo.get_border_count()}\n')
else:
    # Solution found
    print("\t\t   🎉  Winner!  🎉 ")
    print(f'\nDepth: {algo.winner_node.depth}\t '
          f'Cost: {algo.winner_node.depth}\t '
          f'Expanded nodes: {algo.expanded_count}\t '
          f'Border nodes: {algo.get_border_count()}\n')
    road_stack = algo.get_winning_road_stack()

    if print_boolean:
        while road_stack:
            printMap(road_stack.pop())
            time.sleep(print_time)



