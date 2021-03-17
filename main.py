import objects as obj
import mapTraverse as mapFun
import heuristics as heu
import time
import json
import sys
import signal

# Define signal handler for Ctrl+C for ordered interrupt
def signal_handler(sig, frame):
    if algo and not algo.winner_node and start_time:
        print(f'\nAlgorithm Run Interrupted \t\t ⏱  {round(time.time() - start_time, 6)} seconds\n----------------------------------------\n')
        print("\t❌  Failure by Ctrl+C! No solution found with those params. ❌ ")
        print(f'\nExpanded nodes: {algo.expanded_count}')
    print('\nExiting by SIGINT...')
    sys.exit(2)

signal.signal(signal.SIGINT, signal_handler)

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

start_time = time.time()

# Read configurations from file
with open("config.json") as file:
    data = json.load(file)
algo_dic_fun = {'BFS': mapFun.BFS, 'DFS': mapFun.DFS, 'IDDFS': mapFun.IDDFS} 
inf_algo_dic_fun = {'GGS': mapFun.GGS, 'ASS': mapFun.ASS, 'IDASS': mapFun.IDASS}
heu_fun_dic = {1: heu.PlayerToBoxesHeuristic, 2: heu.OneBoxToGoalHeuristic, 
                3: heu.BoxesToGoalsHeuristic, 4: heu.PlayerToBoxesToGoalsHeuristic,
                5: heu.BoxesToGoalsWithDistanceMapHeuristic}

algorithm_name = data["algorithm"]
if algorithm_name in inf_algo_dic_fun:
    heuristic = int(data["heuristic"])
    if heuristic not in heu_fun_dic:
        print("Invalid heuristic number!")
        sys.exit(1)
elif algorithm_name not in algo_dic_fun:
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
goal_map = {}

player_init = None
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
            goal_map[obj.Point(x, y)] = True
        elif character == '$':
            boxes_init.append(obj.Point(x, y))
        elif character == '@':
            if player_init:
                print("Invalid map! Cannot have more than one initial player position.")
                sys.exit(1)
            player_init = obj.Point(x, y)
        elif character == '*':
            static_map[obj.Point(x, y)] = mapFun.Element.Goal
            goal_map[obj.Point(x, y)] = True
            boxes_init.append(obj.Point(x, y))
        elif character == '+':
            if player_init:
                print("Invalid map! Cannot have more than one initial player position.")
                sys.exit(1)
            static_map[obj.Point(x, y)] = mapFun.Element.Goal
            goal_map[obj.Point(x, y)] = True
            player_init = obj.Point(x, y)
        # elif character == ' ': do nothing
        x += 1
    if x > maxX: maxX = x
    y += 1
maxY = y

if len(goal_map) != len(boxes_init):
    print("Invalid map! Cannot have more goals than boxes.")
    sys.exit(1)

init_node = obj.Node(player_init, 0, boxes_init)

end_time = time.time()

file.close()

# Print search params
print('---------------------------------------- \nSearch parameters', '\n\tAlgorithm:\t', algorithm_name)
if algorithm_name == 'IDDFS':
    print('\tIDDFS step:\t', iddfs_step)
elif algorithm_name in inf_algo_dic_fun:
    print('\tHeuristic:\t', heuristic)
print('\tMax. Depth:\t', max_depth, '\n\tLevel:\t\t', level)
print('----------------------------------------')

print(f'Load Configuration & Level Map \t\t ⏱  {round(end_time - start_time, 6)} seconds')
start_time = end_time

if algorithm_name == 'IDDFS':
    algo = algo_dic_fun[algorithm_name](static_map, init_node, max_depth, iddfs_step)
elif algorithm_name in inf_algo_dic_fun:
    if heuristic == 5:
        heu_object = heu_fun_dic[heuristic](static_map, goal_map, maxX, maxY)
    else:    
        heu_object = heu_fun_dic[heuristic](static_map, goal_map)
    algo = inf_algo_dic_fun[algorithm_name](static_map, init_node, max_depth, heu_object)
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
    print(f'\nExpanded nodes: {algo.expanded_count}\n')
else:
    # Solution found
    print("\t\t   🎉  Winner!  🎉 ")
    print(f'\nDepth: {algo.winner_node.depth}\t '
          f'Cost: {algo.winner_node.depth}\t '
          f'Expanded nodes: {algo.expanded_count}\t '
          f'Border nodes: {algo.get_border_count()}\n')

    if print_boolean:
        road_stack = algo.get_winning_road_stack()
        while road_stack:
            node = road_stack.pop()
            printMap(node)
            # TODO: Delete next line when finished testing
            print(node.heuristic_distance)
            time.sleep(print_time)