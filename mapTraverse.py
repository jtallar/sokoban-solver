import enum
import objects as obj

# Possible elements in space
# Eg:   for el in (Element):
#           print(el.name + ' ' + el.value)
class Element(enum.Enum):
    Box = "\U0001F5C2"
    BoxInGoal = "\U0001F5C3"
    Goal = "\U0001F3C1"
    Wall = "\U0001F5FB"
    Player = "\U0001F920"
    PlayerInGoal = "\U0001F929"
    Space = "  "

# General traversal algorithm
class TraverseAlgorithm(object):
    moveFunctionList = [obj.Point.movePointDown, obj.Point.movePointRight, 
        obj.Point.movePointUp, obj.Point.movePointLeft]

    def __init__(self, staticMap, initNode):
        self.staticMap = staticMap
        self.nodeCollection = [initNode]
        self.expandedCount = 0
        self.winnerNode = None
        self.oldNodes = {}
    
    def isAlgorithmOver(self):
        return self.winnerNode or not self.nodeCollection

    def getBorderCount(self):
        return len(self.nodeCollection)

    def checkWinnerNode(self, node):
        if (self.winnerNode):
            return True

        # We assume that # Objectives == # Boxes
        for point in node.boxes:
            if (point not in self.staticMap or self.staticMap[point] != Element.Goal):
                return False
        self.winnerNode = node    
        return True

    def wallInPoint(self, point):
        return point in self.staticMap and self.staticMap[point] == Element.Wall

    def iterate(self):
        pass

    # Returns list of nodes obtained by expanding a node
    def expandNode(self, node):
        newNodes = []
        # Try each possible move
        for move in self.moveFunctionList:
            newPos = move(node.playerPoint)
            # Check for illegal moves
            # If there is a wall in newPos
            if (self.wallInPoint(newPos)):
                continue

            # If there is a box in newPos, check if it can be moved
            boxNextPos = None
            if (newPos in node.boxes):
                boxNextPos = move(newPos)
                if (self.wallInPoint(boxNextPos) or boxNextPos in node.boxes):
                    continue
            
            # If move has already been done
            # TODO: Check repeated nodes
            if (newPos in self.oldNodes):
                continue
            
            self.expandedCount += 1
            newNodeBoxes = list(node.boxes.keys())
            if (boxNextPos is not None):
                newNodeBoxes.remove(newPos)
                newNodeBoxes.append(boxNextPos)

            newNodes.append(obj.Node(newPos, node.depth + 1, newNodeBoxes, node))
        
        return newNodes
    
    def getWinningRoadStack(self):
        road = []
        curNode = self.winnerNode
        while (curNode):
            road.append(curNode)
            curNode = curNode.prevNode

        return road
        
        

class BFS(TraverseAlgorithm):
    
    def __init__(self, staticMap, initNode):
        super().__init__(staticMap, initNode)
    
    # Iteration is based on a Queue collection
    # Should be used paired with algo.isAlgorithmOver() to avoid infinite loops
    def iterate(self):
        """Do one iteration of BFS

        Returns extracted node
        """

        if (super().isAlgorithmOver()):
            return self.winnerNode

        curNode = self.nodeCollection.pop(0)
        if (not super().checkWinnerNode(curNode)):
            self.nodeCollection.extend(super().expandNode(curNode))

        return curNode

        

       
    
    

    

