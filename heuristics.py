import mapTraverse as mt
import objects as obj

INF = 1000000

# Parent class for all Heuristics
class Heuristic(object):
    def __init__(self, static_map, goal_map):
        self.static_map = static_map
        self.goal_map = goal_map
    
    def heuristic(self, node):
        pass

    def dead_point(self, point):
        right = obj.Point.move_point_right(point)
        left = obj.Point.move_point_left(point)
        up = obj.Point.move_point_up(point)
        down = obj.Point.move_point_down(point)
        if (self.is_wall(up) or self.is_wall(down)) and (self.is_wall(left) or self.is_wall(right)):
            return True
        return False

    def is_wall(self, point):
        return point in self.static_map and self.static_map[point]==mt.Element.Wall

    def closest_goal(self, point):
        dist = INF
        for goal_point in self.goal_map:
            aux = point.l1_distance(goal_point)
            if aux < dist:
                dist = aux
        return dist

# Heuristic 1: Sum of manhattan distances from player to boxes not in goals
# Time complexity: O(N), N: number of boxes
class PlayerToBoxesHeuristic(Heuristic):

    def __init__(self, static_map, goal_map):
        super().__init__(static_map, goal_map)

    def heuristic(self, node):
        manhattan = 0
        for box_point in node.boxes:
            if box_point not in self.goal_map:
                if self.dead_point(box_point): return INF
                manhattan += node.player_point.l1_distance(box_point)
        return manhattan

# Heuristic 2: Manhattan distance from any box (not in goal) to closest goal
# Time complexity: O(N), N: number of boxes
class OneBoxToGoalHeuristic(Heuristic):

    def __init__(self, static_map, goal_map):
        super().__init__(static_map, goal_map)

    def heuristic(self, node):
        for box_point in node.boxes:
            if box_point not in self.goal_map:
                if self.dead_point(box_point): return INF
                return self.closest_goal(box_point)
        return 0

# Heuristic 3: Sum of manhattan distances from each box to closest goal (can be repeated)
# Time complexity: O(N^2), N: number of boxes
class BoxesToGoalsHeuristic(Heuristic):
    def __init__(self, static_map, goal_map):
        super().__init__(static_map, goal_map)

    def heuristic(self, node):
        manhattan = 0
        for box_point in node.boxes:
            if box_point not in self.goal_map:
                if self.dead_point(box_point): return INF
                manhattan += self.closest_goal(box_point)
        return manhattan

# Heuristic 4: Sum of Heuristic 1 and Heuristic 3
# Time complexity: O(N) + O(N^2) = O(N^2), N: number of boxes
class PlayerToBoxesToGoalsHeuristic(PlayerToBoxesHeuristic, BoxesToGoalsHeuristic):
    def __init__(self, static_map, goal_map):
        PlayerToBoxesHeuristic.__init__(self, static_map, goal_map)

    def heuristic(self, node):
        return PlayerToBoxesHeuristic.heuristic(self, node) 
                + BoxesToGoalsHeuristic.heuristic(self, node)

# Heuristic 5: Sum of manhattan distances with precalculated distance map 
#              from each box to closest goal (can be repeated)
# Time complexity: O(N), N: number of boxes
class BoxesToGoalsWithDistanceMapHeuristic(Heuristic):
    def __init__(self, static_map, goal_map, max_x, max_y):
        super().__init__(static_map, goal_map)
        self.build_distance_map(max_x, max_y)
    
    # Point -> Distance to closest Goal (0 if goal, no key if wall)
    def build_distance_map(self, max_x, max_y):
        self.distance_map = {}
        for ix in range(max_x):
            for iy in range(max_y):
                point = obj.Point(ix, iy)
                if point in self.goal_map:
                    self.distance_map[point] = 0
                elif point not in self.static_map:
                    self.distance_map[point] = super().closest_goal(point)

    def heuristic(self, node):
        manhattan = 0
        for box_point in node.boxes:
            if box_point not in self.goal_map:
                if self.dead_point(box_point): return INF
                manhattan += self.distance_map[point]
        return manhattan