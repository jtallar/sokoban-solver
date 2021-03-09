import objects as obj
import mapTraverse as mapFun
import time
import json

startTime = time.time()

# Read configurations from file
with open("config.json") as file:
    data = json.load(file)
algorithm = data["algorithm"]
depth = data["depth"]
# TODO: use parameters

# Read map from file
boxesInit = []
staticMap = {}
file = open("level.txt", "r")
y = 0
for line in file:
    x = 0
    for character in line:
        if character == '\n': continue
        x+=1
        if character == '#':
            staticMap[obj.Point(x,y)] = mapFun.Element.Wall
        elif character == '.':
            staticMap[obj.Point(x,y)] = mapFun.Element.Goal
        elif character == '$':
            boxesInit.append(obj.Point(x,y))
        elif (character == '@'):
            playerInit = obj.Point(x,y)
        elif (character == ' '): continue   # TODO: check si hace falta hacer algo o
        elif (character == '*'): continue   #       no deberia pasar en el inicial
        elif (character == '+'): continue
    y+=1

initNode = obj.Node(playerInit, 0, boxesInit)

end_time = time.time()
print(f'Took {end_time - startTime} to read Config and Map')
startTime = end_time

algo = mapFun.BFS(staticMap, initNode)
while (not algo.isAlgorithmOver()):
    curNode = algo.iterate()
    # print(f'{algo.nodeCollection}\n')

end_time = time.time()
print(f'Took {end_time - startTime} to run algorithm')

# TODO: Imprimir parametros de busqueda

# TODO: Move printing to function/other place, add return in failure instead of if/else
if (not algo.winnerNode):
    # Solution not found
    print("Failure!")
else:
    # Solution found
    print("Success!")
    print(f'Depth: {algo.winnerNode.depth}; Expanded nodes: {algo.expandedCount}; Border nodes: {algo.getBorderCount()}')
    roadStack = algo.getWinningRoadStack()

    # TODO: Print map instead of nodes
    while (roadStack):
        print(f'{roadStack.pop()}\n')