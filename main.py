import objects as obj
import mapTraverse as mapFun

# TODO: Read configurations from file
# TODO: Read map from file
playerInit = obj.Point(10, 10)
boxesInit = [obj.Point(10, 9), obj.Point(11, 10)]

goalsInit = [obj.Point(7, 7), obj.Point(7, 6)]
wallInit = [obj.Point(10, 11), obj.Point(10, 8)]

staticMap = {}
for point in goalsInit:
    staticMap[point] = mapFun.Element.Goal
for point in wallInit:
    staticMap[point] = mapFun.Element.Wall

initNode = obj.Node(playerInit, 0, boxesInit)
print(initNode)

for el in (mapFun.Element):
    print(el.name + ' ' + el.value)

algo = mapFun.TraverseAlgorithm(staticMap)
print(algo.expandNode(initNode))