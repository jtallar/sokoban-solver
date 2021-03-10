import objects as obj
import mapTraverse as mapFun
import json

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
