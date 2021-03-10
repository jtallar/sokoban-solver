import objects as obj
import mapTraverse as mapFun
import initMap as init
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

start_time = time.time()

# Read configurations from file
with open("config.json") as file:
    data = json.load(file)
algo_dic_fun = {'BFS': mapFun.BFS, 'DFS': mapFun.DFS}
algorithm = data["algorithm"]
if algorithm not in algo_dic_fun:
    print("Invalid algorithm!")
    sys.exit(1)

depth = data["depth"]
level = 'level_' + data["level"] + '.txt'
# TODO: use parameters

# Read map from file
boxes_init = []
static_map = {}
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
    if x > maxX: maxX = x
    y += 1
maxY = y

# TODO: Create simple map validation?
#       No 2 player_init, # boxes <= # goals
init_node = obj.Node(player_init, 0, boxes_init)

end_time = time.time()

# Print search params
print('---------------------------------------- \nSearch parameters', '\n\tAlgorithm:\t', algorithm)
print('\tMax. Depth:\t', depth, '\n----------------------------------------')

print(f'Load Configuration & Level Map \t\t 🕓 {round(end_time - start_time, 6)} seconds')
start_time = end_time

algo = algo_dic_fun[algorithm](static_map, init_node)
while not algo.is_algorithm_over():
    curr_node = algo.iterate()
    # print(f'{algo.node_collection}\n')

end_time = time.time()
print(f'Algorithm Run Completed \t\t 🕓 {round(end_time - start_time, 6)} seconds\n----------------------------------------\n')

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
          # costo de la solucion se pone algo?
    road_stack = algo.get_winning_road_stack()

    # TODO: Print map instead of nodes
    while road_stack:
        printMap(road_stack.pop())



