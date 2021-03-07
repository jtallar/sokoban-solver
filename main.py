import objects as obj
import mapTraverse as mapFun

# TODO: Read configurations from file
# TODO: Read map from file
playerInit = obj.Point(10, 10)
boxesInit = [obj.Point(5, 5), obj.Point(6, 6)]

goalsInit = [obj.Point(7, 7), obj.Point(7, 6)]
wallInit = [obj.Point(1, 1), obj.Point(2, 2)]

staticMap = {}
for point in goalsInit:
    staticMap[point] = mapFun.Element.Goal
for point in wallInit:
    staticMap[point] = mapFun.Element.Wall

print(playerInit)
initNode = obj.Node(playerInit, 0, boxesInit)
print(initNode)

for el in (mapFun.Element):
    print(el.name + ' ' + el.value)