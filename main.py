import objects as obj
import mapTraverse as mapFun
import time

startTime = time.time()
# TODO: Read configurations from file
# TODO: Read map from file
# playerInit = obj.Point(10, 10)
# boxesInit = [obj.Point(10, 9), obj.Point(11, 10)]
# goalsInit = [obj.Point(7, 7), obj.Point(7, 6)]
# wallInit = [obj.Point(10, 11), obj.Point(10, 8)]

playerInit = obj.Point(2, 2)
boxesInit = [obj.Point(3, 2)]
goalsInit = [obj.Point(5, 2)]
wallInit = [obj.Point(1, 1), obj.Point(2, 1), obj.Point(3, 1), obj.Point(4, 1), obj.Point(5, 1), obj.Point(6, 1),
    obj.Point(1, 4), obj.Point(2, 4), obj.Point(3, 4), obj.Point(4, 4), obj.Point(5, 4), obj.Point(6, 4),
    obj.Point(1, 2), obj.Point(6, 2), obj.Point(1, 3), obj.Point(6, 3)]

staticMap = {}
for point in goalsInit:
    staticMap[point] = mapFun.Element.Goal
for point in wallInit:
    staticMap[point] = mapFun.Element.Wall

initNode = obj.Node(playerInit, 0, boxesInit)

end_time = time.time()
print(f'Took {end_time - startTime} to read Config and Map')
startTime = end_time

algo = mapFun.BFS(staticMap, initNode)
i = 0
while (not algo.isAlgorithmOver() and i <= 8):
    curNode = algo.iterate()
    print(curNode)
    i += 1

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