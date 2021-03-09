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
level = 'level_' + data["level"] + '.txt'
# TODO: use parameters

# Read map from file
boxesInit = []
staticMap = {}
file = open(level, "r")
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
        elif (character == '*'): 
            staticMap[obj.Point(x,y)] = mapFun.Element.Goal
            boxesInit.append(obj.Point(x,y))
        elif (character == '+'): 
            staticMap[obj.Point(x,y)] = mapFun.Element.Goal
            playerInit = obj.Point(x,y)
        elif (character == ' '): continue
    y+=1

# TODO: Metemos alguna validacion de mapa simple?
#       Que no haya 2 playerInit, que haya # boxes <= # goals
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