import enum
import objects as obj
import heapq as hq

# Possible elements in space
# Eg:   for el in (Element):
#           print(el.name + ' ' + el.value)
class Element(enum.Enum):
    Box = "\U0001F5C2 "
    BoxInGoal = "\U0001F5C3 "
    Goal = "\U0001F3C1"
    Wall = "\U0001F9F1"
    Player = "\U0001F920"
    PlayerInGoal = "\U0001F9D0"    # TODO: check emoji
    Space = "  "


# General traversal algorithm
class TraverseAlgorithm(object):
    moveFunctionList = [obj.Point.move_point_down, obj.Point.move_point_right,
                        obj.Point.move_point_up, obj.Point.move_point_left]

    def __init__(self, static_map, init_node, max_depth, max_expanded_nodes):
        self.static_map = static_map
        self.node_collection = [init_node]
        self.max_depth = max_depth
        self.max_expanded_nodes = max_expanded_nodes
        self.expanded_count = 0
        self.winner_node = None
        self.old_nodes = {}
        # Add initial node to old nodes. Node is old when seen, not when expanded!
        self.mark_node_as_old(init_node)

    def is_algorithm_over(self):
        return self.winner_node or not self.node_collection

    def get_border_count(self):
        return len(self.node_collection)

    def check_winner_node(self, node):
        if self.winner_node:
            return True

        # We assume that # Objectives == # Boxes
        for point in node.boxes:
            if point not in self.static_map or self.static_map[point] != Element.Goal:
                return False
        self.winner_node = node
        return True

    def wall_in_point(self, point):
        return point in self.static_map and self.static_map[point] == Element.Wall

    def iterate(self):
        pass

    def mark_node_as_old(self, node):
        self.old_nodes[node] = True

    def is_node_old(self, node):
        return node in self.old_nodes

    # Returns list of nodes obtained by expanding a node
    def expand_node(self, node):
        # If max_depth reached or max_expanded_nodes reached, do not expand
        if node.depth >= self.max_depth or self.expanded_count >= self.max_expanded_nodes:
            return []

        self.expanded_count += 1

        new_nodes = []
        # Try each possible move
        for move in self.moveFunctionList:
            new_pos = move(node.player_point)
            # Check for illegal moves
            # If there is a wall in new_pos
            if self.wall_in_point(new_pos):
                continue

            # If there is a box in new_pos, check if it can be moved
            box_next_pos = None
            if new_pos in node.boxes:
                box_next_pos = move(new_pos)
                if self.wall_in_point(box_next_pos) or box_next_pos in node.boxes:
                    continue

            new_node_boxes = list(node.boxes.keys())
            if box_next_pos:  # eq to (box_next_pos is not None)
                new_node_boxes.remove(new_pos)
                new_node_boxes.append(box_next_pos)

            new_node = obj.Node(new_pos, node.depth + 1, new_node_boxes, node)

            # If move has already been done, skip.
            if self.is_node_old(new_node):
                continue
            # If not, add it as old
            self.mark_node_as_old(new_node)

            new_nodes.append(new_node)

        return new_nodes

    def get_winning_road_stack(self):
        road = []
        cur_node = self.winner_node
        while cur_node:
            road.append(cur_node)
            cur_node = cur_node.prev_node

        return road

# Breadth First Search
class BFS(TraverseAlgorithm):

    def __init__(self, static_map, init_node, max_depth, max_expanded_nodes):
        super().__init__(static_map, init_node, max_depth, max_expanded_nodes)

    # Iteration is based on a Queue collection
    # Should be used paired with algo.isAlgorithmOver() to avoid infinite loops
    def iterate(self):
        """Do one iteration of BFS

        Returns extracted node
        """

        if super().is_algorithm_over():
            return self.winner_node

        cur_node = self.node_collection.pop(0)
        if not super().check_winner_node(cur_node):
            self.node_collection.extend(super().expand_node(cur_node))

        return cur_node

# Depth First Search
class DFS(TraverseAlgorithm):

    def __init__(self, static_map, init_node, max_depth, max_expanded_nodes):
        super().__init__(static_map, init_node, max_depth, max_expanded_nodes)

    # Iteration is based on a Stack collection
    # Should be used paired with algo.isAlgorithmOver() to avoid infinite loops
    def iterate(self):
        """Do one iteration of DFS

        Returns extracted node
        """

        if super().is_algorithm_over():
            return self.winner_node

        cur_node = self.node_collection.pop()
        if not super().check_winner_node(cur_node):
            self.node_collection.extend(super().expand_node(cur_node))

        return cur_node

# Iterative Deepening Depth First Search
class IDDFS(TraverseAlgorithm):

    def __init__(self, static_map, init_node, max_depth, max_expanded_nodes, depth_step=float("inf")):
        self.limit_nodes = []
        self.depth_step = depth_step
        self.cur_max_depth = depth_step
        super().__init__(static_map, init_node, max_depth, max_expanded_nodes)

    # Iteration is based on a Stack collection
    # Should be used paired with algo.isAlgorithmOver() to avoid infinite loops
    def iterate(self):
        """Do one iteration of IDDFS

        Returns extracted node
        """

        if super().is_algorithm_over():
            return self.winner_node

        cur_node = self.node_collection.pop()
        if not super().check_winner_node(cur_node):
            if cur_node.depth < self.cur_max_depth:
                self.node_collection.extend(super().expand_node(cur_node))
            else:
                self.limit_nodes.append(cur_node)

            # When empty, try with limit_nodes and more depth
            if not self.node_collection and self.limit_nodes:
                self.node_collection = self.limit_nodes
                self.limit_nodes = []
                self.cur_max_depth += self.depth_step
            

        return cur_node

class InformedTraverseAlgorithm(TraverseAlgorithm):
    def __init__(self, static_map, init_node, max_depth, max_expanded_nodes, heuristic_instance, constructor):
        init_node = constructor(init_node, heuristic_instance.heu(init_node))
        super().__init__(static_map, init_node, max_depth, max_expanded_nodes)
        self.heuristic_instance = heuristic_instance
        self.constructor = constructor

    # Iteration is based on a Priority Queue collection
    # Should be used paired with algo.isAlgorithmOver() to avoid infinite loops
    def iterate(self):
        """Do one iteration of Informed Algorithm Method

        Returns extracted node
        """

        if super().is_algorithm_over():
            return self.winner_node

        cur_node = hq.heappop(self.node_collection)
        if not super().check_winner_node(cur_node):
            new_base_nodes = super().expand_node(cur_node)
            for base_node in new_base_nodes:
                hq.heappush(self.node_collection, self.constructor(base_node, self.heuristic_instance.heu(base_node)))

        return cur_node

# Global Greedy Search
class GGS(InformedTraverseAlgorithm):
    def __init__(self, static_map, init_node, max_depth, max_expanded_nodes, heuristic_instance):
        super().__init__(static_map, init_node, max_depth, max_expanded_nodes, heuristic_instance, obj.HeuristicNode)

# A* (Star) Search
class ASS(InformedTraverseAlgorithm):
    def __init__(self, static_map, init_node, max_depth, max_expanded_nodes, heuristic_instance):
        super().__init__(static_map, init_node, max_depth, max_expanded_nodes, heuristic_instance, obj.AStarNode)

# Iterative Deepening A* (Star) Search
class IDASS(InformedTraverseAlgorithm):

    def __init__(self, static_map, init_node, max_depth, max_expanded_nodes, heuristic_instance):
        self.limit_nodes = []
        super().__init__(static_map, init_node, max_depth, max_expanded_nodes, heuristic_instance, obj.AStarNode)
        self.cur_limit = self.node_collection[0].f_sum
        self.next_limit = float("inf")

    # Iteration is based on a Stack collection (DFS iteration with f(n) limit)
    # Should be used paired with algo.isAlgorithmOver() to avoid infinite loops
    def iterate(self):
        """Do one iteration of IDASS

        Returns extracted node
        """

        if super().is_algorithm_over():
            return self.winner_node

        cur_node = self.node_collection.pop()
        if not super().check_winner_node(cur_node):
            if cur_node.f_sum <= self.cur_limit:
                new_base_nodes = super().expand_node(cur_node)
                for base_node in new_base_nodes:
                    self.node_collection.append(self.constructor(base_node, self.heuristic_instance.heu(base_node)))
            else:
                if cur_node.f_sum < self.next_limit:
                    self.next_limit = cur_node.f_sum
                self.limit_nodes.append(cur_node)

            # When empty, try with limit_nodes and more depth
            if not self.node_collection and self.limit_nodes:
                self.node_collection = self.limit_nodes
                self.limit_nodes = []
                self.cur_limit = self.next_limit
                self.next_limit = float("inf")

        return cur_node
