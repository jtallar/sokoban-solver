import mapTraverse as mt
import objects as obj

INF = 10000

class Heuristic:

    @staticmethod
    def h1(node, static_map, goal_map):   
        manhattan = 0
        for box_point in node.boxes.keys():
            if box_point not in goal_map:
                dead = dead_move(box_point, static_map)
                if dead > 0: return dead
                manhattan += distance(node.player_point, box_point)
        return manhattan

    @staticmethod
    def h2(node, static_map, goal_map):
        manhattan = 0
        for box_point in node.boxes.keys():
            if node.boxes[box_point] and box_point not in goal_map:
                dead = dead_move(box_point, static_map)
                if dead > 0: return dead
                manhattan = closest_goal(box_point, goal_map)
                break
        return manhattan

    @staticmethod
    def h3(node, static_map, goal_map):
        manhattan = 0
        for box_point in node.boxes.keys():
            if node.boxes[box_point] and box_point not in goal_map:
                dead = dead_move(box_point, static_map)
                if dead > 0: return dead
                manhattan += closest_goal(box_point, goal_map)
        return manhattan

    @staticmethod
    def h4(node, static_map, goal_map): 
        return Heuristic.h1(node, static_map, goal_map) + Heuristic.h3(node, static_map, goal_map)

def dead_move(point, static_map):
    right = obj.Point.move_point_right(point)
    left = obj.Point.move_point_left(point)
    up = obj.Point.move_point_up(point)
    down = obj.Point.move_point_down(point)
    if (is_wall(up, static_map) or is_wall(down, static_map)) and (is_wall(left, static_map) or is_wall(right, static_map)):
        return INF
    return 0

def distance(point_a, point_b):
    return abs(point_a.x - point_b.x) + abs(point_a.y - point_b.y)

def is_wall(point, static_map):
    return point in static_map and static_map[point]==mt.Element.Wall

def closest_goal(point, goal_map):
    dist = INF
    for goal in goal_map.keys():
        aux = distance(point, goal)
        if aux < dist:
            dist = aux
    return dist