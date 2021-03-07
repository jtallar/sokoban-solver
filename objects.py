# Point with positive coordinates
# (0,0) is at top left corner
class Point(object):

    def __init__(self, x=0, y=0):
        """Returns a Point object with the given coordinates

        Parameters
        ----------
        x : int
            Horizontal coordinate
        y : int
            Vertical coordinate
        """

        self.x = x
        self.y = y
    
    def __str__(self):
        return self.__repr__()
    
    def __repr__(self):
        return "Point(%s,%s)"%(self.x, self.y)

    def moveLeft(self):
        if (self.x <= 0):
            raise ValueError("X cannot be negative!")
        self.x = self.x - 1
    
    def moveRight(self, maxX=float("inf")):
        if (self.x >= maxX):
            raise ValueError("X cannot be higher than maxX!")
        self.x = self.x + 1
    
    def moveUp(self):
        if (self.y <= 0):
            raise ValueError("Y cannot be negative!")
        self.y = self.y - 1
    
    def moveDown(self, maxY=float("inf")):
        if (self.y >= maxY):
            raise ValueError("Y cannot be higher than maxY!")
        self.y = self.y + 1
    
    # Static methods for point objects, returns new Point objects
    @staticmethod
    def movePointLeft(point):
        if (point.x <= 0):
            raise ValueError("X cannot be negative!")
        return self.__class__(point.x - 1, point.y)
    
    @staticmethod
    def movePointRight(point, maxX=float("inf")):
        if (point.x >= maxX):
            raise ValueError("X cannot be higher than maxX!")
        return self.__class__(point.x + 1, point.y)
    
    @staticmethod
    def movePointUp(point):
        if (point.y <= 0):
            raise ValueError("Y cannot be negative!")
        return self.__class__(point.x, point.y - 1)

    @staticmethod
    def movePointDown(point, maxY=float("inf")):
        if (point.y >= maxY):
            raise ValueError("Y cannot be higher than maxY!")
        return self.__class__(point.x, point.y + 1)

    # Define hash and eq methods to allow key usage
    def __hash__(self):
        return hash((self.x, self.y))
    
    def __eq__(self, other):
        return (self.x, self.y) == (other.x, other.y)
    
    def __ne__(self, other):
        return not(self == other)


class Node(object):
    
    # Create a node
    def __init__(self, playerPoint, depth, boxPointsList, prevNode=None):
        """Create a node used for sokoban

        Parameters
        ----------
        playerPoint : Point
            Point with player coordinates
        depth : int
            Node depth in tree
        boxPointsList : list
            List of box points in map
        prevNode : Node, optional
            Node object of parent node in tree
        """

        self.playerPoint = playerPoint
        self.depth = depth
        self.prevNode = prevNode
        self.boxes = {}
        for point in boxPointsList:
            self.boxes[point] = True
    
    def __str__(self):
        return self.__repr__()
    
    def __repr__(self):
        return "Node(player=%s,depth=%s,boxes=%s)"%(self.playerPoint, self.depth, self.boxes)
        

