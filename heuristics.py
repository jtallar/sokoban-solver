
class Heuristic:

    @staticmethod
    def h1(node, static_map):   # ,goals_map
        manhattan = 0
        for box_point in node.boxes.keys():
            if node.boxes[box_point]:   # and box_point not in goals_map
                manhattan += distance(node.player_point, box_point)
        print(manhattan)
        return manhattan

    @staticmethod
    def h2(node, static_map):   # ,goals_map
        manhattan = 0
        for box_point in node.boxes.keys():
            if node.boxes[box_point]:   # and box_point not in goals_map
                manhattan = distance(box_point, objetivo mas cercano)
                break
        return manhattan

    @staticmethod
    def h3(node, static_map):   # ,goals_map
        manhattan = 0
        for box_point in node.boxes.keys():
            if node.boxes[box_point]:   # and box_point not in goals_map
                manhattan = distance(box_point, objetivo mas cercano)
                continue
        return manhattan

    @staticmethod
    def h4(node, static_map):   # ,goals_map
        h = 0
        return h

    def dead_move(node, static_map):
        for i in static_map:
            continue
        return 0

def distance(point_a, point_b):
    return abs(point_a.x - point_b.x) + abs(point_a.y - point_b.y)

