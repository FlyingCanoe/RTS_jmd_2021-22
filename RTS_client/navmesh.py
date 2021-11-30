from math import floor

from helper import Helper


class NavNode:
    def __init__(self, mesh, x1, y1, x2, y2):
        self.navmesh = mesh

        self.x1 = x1
        self.y1 = y1

        self.x2 = x2
        self.y2 = y2

        self.adjacent = set([])

    def add_adjacent(self, new_adjacent):
        my_centre_x, my_centre_y = self.centre()
        other_centre_x, other_centre_y = self.centre()

        cost = Helper.calcDistance(my_centre_x, my_centre_y, other_centre_x, other_centre_y)
        self.adjacent.add({"node": new_adjacent, "cost": cost})

    def reset_adjacent(self):
        self.adjacent = set([])

    def size_x(self):
        return abs(self.x1 - self.x2) + 1

    def size_y(self):
        return abs(self.y1 - self.y2) + 1

    def split(self):
        if self.size_x() > self.size_y():
            left_x1 = self.x1
            left_x2 = self.x1 + int(floor(self.size_x() / 2))

            right_x1 = left_x2 + 1
            right_x2 = self.x2

            left_node = NavNode(self.navmesh, left_x1, self.y1, left_x2, self.y2)
            right_node = NavNode(self.navmesh, right_x1, self.y1, right_x2, self.y2)
            return left_node, right_node
        else:
            down_y1 = self.y1
            down_y2 = self.y1 + int(floor(self.size_y() / 2))

            up_y1 = down_y2 + 1
            up_y2 = self.y2

            down_node = NavNode(self.navmesh, self.x1, down_y1, self.x2, down_y2)
            up_node = NavNode(self.navmesh, self.x1, up_y1, self.x2, up_y2)
            return down_node, up_node

    def centre(self):
        x = self.x2 - self.x1 / 2
        y = self.y1 - self.y2 / 2
        return x, y


class NavMesh:
    def __init__(self):
        self.travarsable = []
        self.obstacle = []

    def add_obstacle(self, x1, y1, x2, y2):
        obstacle = NavNode(self, x1, y1, x2, y2)

        for node in self.travarsable:
            if self.check_contient(obstacle, node):
                lhs, rhs = node.split()
                self.travarsable.remove(node)
                self.travarsable.append(lhs)
                self.travarsable.append(rhs)
                return self.add_obstacle(x1, y1, x2, y2)
        self.obstacle.append(NavNode)
        self.update_adjacent()

    def check_contient(self, node1, node2):
        if (node2.x1 <= node1.x1 <= node2.x2) or (node2.x1 <= node1.x2 <= node2.x2):
            if (node2.y1 <= node1.y1 <= node2.y2) or (node2.y1 <= node1.y2 <= node2.y2):
                return True
        if (node1.x1 <= node2.x1 <= node1.x2) or (node1.x1 <= node2.x2 <= node1.x2):
            if (node1.y1 <= node2.y1 <= node1.y2) or (node1.y1 <= node2.y2 <= node1.y2):
                return True
        return False

    def check_adjacent(self, node1, node2):
        # check si ils sont adjacent en x
        if node1.x1 - node2.x2 == 1 or node2.x1 - node1.x2:
            # check si node2 est aligner a la node1 en y
            if (node2.y1 <= node1.y1 <= node2.y2) or (node2.y1 <= node1.x2 <= node2.y2):
                return True
            # check si node1 est aligner a la node2 en y
            elif (node1.y1 <= node2.y1 <= node1.x2) or (node1.y1 <= node2.y2 <= node1.x2):
                return True

        # check si ils sont adjacent en y
        if node1.y1 - node2.y2 == 1 or node2.y1 - node1.x2:
            # check si node2 est aligner a la node1 en x
            if (node2.x1 <= node1.x1 <= node2.x2) or (node2.x1 <= node1.x2 <= node2.x2):
                return True
            # check si node1 est aligner a la node2 en x
            elif (node1.x1 <= node2.x1 <= node1.x2) or (node1.x1 <= node2.x2 <= node1.x2):
                return True

        return False

    def update_adjacent(self):
        for i in self.travarsable:
            i.reset_adjacent()
            for j in self.travarsable:
                if self.check_adjacent(i, j):
                    i.add_adjacent(j)

    # A * finds a path from start to goal.
    # h is the heuristic function.h(n) estimates the cost to reach goal from node n.
    def A_Star(self, start: NavNode, goal: NavNode, h):

        # The set of discovered nodes that may need to be(re -) expanded.
        # Initially, only the start node is known.
        # This is usually implemented as a min - heap or priority queue rather than a hash - set.
        open_set = set([start])

        # For node n, cameFrom[n] is the node immediately preceding it on the cheapest path from start
        # to n currently known.
        came_from = {}

        # For node n, g_score[n] is the cost of the cheapest path from start to n currently known.
        g_score = {}
        # For node n, f_score[n] := g_score[n] + h(n).f_score[n] represents our current best guess as to
        # how short a path from start to finish can be if it goes through n.
        f_score = {}

        for node in self.travarsable:
            g_score[node] = float('inf')
            f_score[node] = float('inf')
        g_score[start] = 0
        f_score[start] = h(start)

        while len(open_set) != 0:
            # This operation can occur in O(1) time if openSet is a min - heap or a priority queue
            f_score.items()
            current: NavNode = min(f_score.items(), key=lambda x: x[1])[0]
            if current == goal:
                return reconstruct_path(came_from, current)

            open_set.remove(current)
            for neighbor, cost in current.adjacent:
                # d(current, neighbor) is the weight of the edge from current to neighbor
                # tentative_g_score is the distance from start to

                # the neighbor through current
                tentative_g_score = g_score[current] + cost
                if tentative_g_score < g_score[neighbor]:
                    # This path to neighbor is better than any previous one. Record it!
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g_score
                    f_score[neighbor] = tentative_g_score + h(neighbor)
                    if neighbor not in open_set:
                        open_set.add(neighbor)

        # Open set is empty but goal was never reached
        return None


def reconstruct_path(came_from: dict, current):
    total_path = [current]
    while current in came_from.keys():
        current = came_from[current]
        total_path.insert(0, current.centre())
    return total_path


