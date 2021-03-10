import objects as obj
# import mapTraverse as mapFun
import json

# Read configurations from file
with open("config.json") as file:
    data = json.load(file)
algorithm = data["algorithm"]
depth = data["depth"]

# Read map from file
boxesInit = []
goalsInit = []
wallInit = []
file = open("sample.txt", "r")
y = 0
for line in file:
    x = 0
    for character in line:
        if character == '\n':
            continue
        x += 1
        if character == '#':
            wallInit.append(obj.Point(x, y))
        elif character == '$':
            boxesInit.append(obj.Point(x, y))
        elif character == '.':
            goalsInit.append(obj.Point(x, y))
        elif character == '@':
            playerInit = obj.Point(x, y)
        elif character == ' ':
            continue
        elif character == '*':
            continue
        elif character == '+':
            continue
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
