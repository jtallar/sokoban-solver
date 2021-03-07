import objects as obj

# TODO: Read configurations from file
# TODO: Read map from file
playerInit = obj.Point(10, 10)
boxesInit = [obj.Point(5, 5), obj.Point(6, 6)]

goalsInit = [obj.Point(7, 7), obj.Point(7, 6)]
goalDic = {}
for point in goalsInit:
    goalDic[point] = True
wallInit = [obj.Point(1, 1), obj.Point(2, 2)]
wallDic = {}
for point in wallInit:
    wallDic[point] = True

print(playerInit)
initNode = obj.Node(playerInit, 0, boxesInit)
print(initNode)
