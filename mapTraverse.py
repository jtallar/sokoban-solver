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
    moveFunctionList = [obj.Point.move_point_down, obj.Point.move_point_right,
                        obj.Point.move_point_up, obj.Point.move_point_left]

    def __init__(self, static_map, init_node):
        self.static_map = static_map
        self.node_collection = [init_node]
        self.expanded_count = 0
        self.winner_node = None
        self.old_nodes = {}
        self.old_node_count = 0
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
        if node.player_point not in self.old_nodes:
            self.old_nodes[node.player_point] = {}

        for box in node.boxes:
            if box not in self.old_nodes[node.player_point]:
                self.old_nodes[node.player_point][box] = {}
            self.old_nodes[node.player_point][box][self.old_node_count] = True

        self.old_node_count += 1

    def is_node_old(self, node):
        if node.player_point not in self.old_nodes:
            return False

        (first, ids) = (True, [])
        for box in node.boxes:
            if box not in self.old_nodes[node.player_point]:
                return False
            if first:
                first = False
                ids = self.old_nodes[node.player_point][box].keys()
            else:
                new_ids = []
                for _id in ids:
                    if _id in self.old_nodes[node.player_point][box]:
                        new_ids.append(_id)
                ids = new_ids
                if not ids:
                    return False

        return not not ids

    # Returns list of nodes obtained by expanding a node
    def expand_node(self, node):
        # TODO: Check if this count goes here. Should only add when it has children?
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


class BFS(TraverseAlgorithm):

    def __init__(self, static_map, init_node):
        super().__init__(static_map, init_node)

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

class DFS(TraverseAlgorithm):

    def __init__(self, static_map, init_node):
        super().__init__(static_map, init_node)

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



