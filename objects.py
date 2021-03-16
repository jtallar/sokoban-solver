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
        return "Point(%s,%s)" % (self.x, self.y)

    def move_left(self):
        if self.x <= 0:
            raise ValueError("X cannot be negative!")
        self.x = self.x - 1

    def move_right(self, max_x=float("inf")):
        if self.x >= max_x:
            raise ValueError("X cannot be higher than maxX!")
        self.x = self.x + 1

    def move_up(self):
        if self.y <= 0:
            raise ValueError("Y cannot be negative!")
        self.y = self.y - 1

    def move_down(self, max_y=float("inf")):
        if self.y >= max_y:
            raise ValueError("Y cannot be higher than maxY!")
        self.y = self.y + 1

    # Static methods for point objects, returns new Point objects
    @staticmethod
    def move_point_left(point):
        if point.x <= 0:
            raise ValueError("X cannot be negative!")
        return Point(point.x - 1, point.y)

    @staticmethod
    def move_point_right(point, max_x=float("inf")):
        if point.x >= max_x:
            raise ValueError("X cannot be higher than maxX!")
        return Point(point.x + 1, point.y)

    @staticmethod
    def move_point_up(point):
        if point.y <= 0:
            raise ValueError("Y cannot be negative!")
        return Point(point.x, point.y - 1)

    @staticmethod
    def move_point_down(point, max_y=float("inf")):
        if point.y >= max_y:
            raise ValueError("Y cannot be higher than maxY!")
        return Point(point.x, point.y + 1)

    # Define hash and eq methods to allow key usage
    def __hash__(self):
        return hash((self.x, self.y))

    def __eq__(self, other):
        return (self.x, self.y) == (other.x, other.y)

    def __ne__(self, other):
        return not (self == other)


class Node(object):

    # Create a node
    def __init__(self, player_point, depth, box_points_list, prev_node=None):
        """Create a node used for sokoban

        Parameters
        ----------
        player_point : Point
            Point with player coordinates
        depth : int
            Node depth in tree
        box_points_list : list
            List of box points in map
        prev_node : Node, optional
            Node object of parent node in tree
        """

        self.player_point = player_point
        self.depth = depth
        self.prev_node = prev_node
        self.boxes = {}
        for point in box_points_list:
            self.boxes[point] = True

    def copy_node(self, node):
        """Create a node based on another node.
        References still exist!

        Parameters
        ----------
        node : Node
            Node object to copy
        """
        self.player_point = node.player_point
        self.depth = node.depth
        self.prev_node = node.prev_node
        self.boxes = node.boxes

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return "Node(player=%s,depth=%s,boxes=%s)" % (self.player_point, self.depth, self.boxes)

    # Define hash and eq methods to allow key usage
    def __hash__(self):
        return hash(self.player_point) + 31 * hash(frozenset(self.boxes.items()))

    def __eq__(self, other):
        if self.player_point != other.player_point:
            return False
        for box_point in self.boxes:
            if box_point not in other.boxes:
                return False
        return True

    def __ne__(self, other):
        return not (self == other)

class HeuristicNode(Node):

    # Create a Heuristic Node based on a Node and an estimated h(n)
    def __init__(self, node, heuristic_distance):
        """Create a node used for sokoban

        Parameters
        ----------
        node : Node
            Node to replicate and take as own (same references)
        heuristic_function : int
            Estimated distance from this node to finish
        """
        super().copy_node(node)
        self.heuristic_distance = heuristic_distance

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return "HeuristicNode(h(n)=%s,%s)" % (self.heuristic_distance, super().__repr__())
    
    def __lt__(self, other):
        if self.heuristic_distance == other.heuristic_distance:
            return self.depth < other.depth
        return self.heuristic_distance < other.heuristic_distance

class AStarNode(HeuristicNode):
    # Create an AStarNode based on a Node and an estimated h(n)
    def __init__(self, node, heuristic_distance):
        super().__init__(node, heuristic_distance)
        self.f_sum = self.heuristic_distance + self.depth

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return "AStarNode(f(n)=%s,%s)" % (self.f_sum, super().__repr__())
    
    def __lt__(self, other):
        if self.f_sum == other.f_sum:
            return self.heuristic_distance < other.heuristic_distance
        return self.f_sum < other.f_sum

