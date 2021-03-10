import objects as obj
import mapTraverse as mapFun
import json

def printMap(node, maxX, maxY, static_map):
    line = ''
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
        line = ''
    print('\n')

# Read configurations from file
with open("config.json") as file:
    data = json.load(file)
algorithm = data["algorithm"]
depth = data["depth"]

# Read map from file
boxes_init = []
static_map = {}
file = open("level_easy.txt", "r")
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

# Walls:                    #
# Boxes:                    $
# Goals:                    .
# Free squares:            ' '
# The Sokoban / the player: @
# Boxes on goals:           *
# The Sokoban on a goal:    +


# testing print

# print('-- walls --')
# for wall in wallInit:
#     print(wall)
# print('\n -- boxes -- ')
# for box in boxesInit:
#     print(box)
# print('\n -- goals -- ')
# for goal in goalsInit:
#     print(goal)
# print('\n -- player --', playerInit)
