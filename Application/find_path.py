__author__ = 'Edwin Clement'
# A* Shortest Path Algorithm
# http://en.wikipedia.org/wiki/A*
# FB - 201012256
from heapq import heappush, heappop
import math


class node:
    # current position
    xPos = 0
    yPos = 0
    # total distance already travelled to reach the node
    distance = 0
    # priority = distance + remaining distance estimate
    priority = 0  # smaller: higher priority

    def __init__(self, xPos, yPos, distance, priority):
        self.xPos = xPos
        self.yPos = yPos
        self.distance = distance
        self.priority = priority

    def __lt__(self, other): # for priority queue
        return self.priority < other.priority

    def updatePriority(self, xDest, yDest):
        self.priority = self.distance + self.estimate(xDest, yDest) * 10 # A*
    # give better priority to going straight instead of diagonally

    def nextdistance(self, i): # i: direction
        if i % 2 == 0:
            self.distance += 10
        else:
            self.distance += 14

    # Estimation function for the remaining distance to the goal.
    def estimate(self, xDest, yDest):
        xd = xDest - self.xPos
        yd = yDest - self.yPos
        # Euclidian Distance
        d = math.sqrt(xd * xd + yd * yd)
        # Manhattan distance
        # d = abs(xd) + abs(yd)
        # Chebyshev distance
        # d = max(abs(xd), abs(yd))
        return (d)


# A-star algorithm.
# Path returned will be a string of digits of directions.
class AStar:
    def __init__(self, parent):
        self.parent = parent

    def pathFind(self, the_map, directions, dx, dy, xStart, yStart, xFinish, yFinish):
        n, m = 100, 100
        closed_nodes_map = []  # map of closed (tried-out) nodes
        open_nodes_map = []  # map of open (not-yet-tried) nodes
        dir_map = []  # map of directions
        row = [0] * n
        for i in range(m): # create 2d arrays
            closed_nodes_map.append(list(row))
            open_nodes_map.append(list(row))
            dir_map.append(list(row))

        pq = [[], []]  # priority queues of open (not-yet-tried) nodes
        pqi = 0  # priority queue index
        # create the start node and push into list of open nodes
        n0 = node(xStart, yStart, 0, 0)
        n0.updatePriority(xFinish, yFinish)
        heappush(pq[pqi], n0)
        open_nodes_map[yStart][xStart] = n0.priority # mark it on the open nodes map

        # A* search
        while len(pq[pqi]) > 0:
            # get the current node w/ the highest priority
            # from the list of open nodes
            n1 = pq[pqi][0] # top node
            n0 = node(n1.xPos, n1.yPos, n1.distance, n1.priority)
            x = n0.xPos
            y = n0.yPos
            heappop(pq[pqi]) # remove the node from the open list
            open_nodes_map[y][x] = 0
            # mark it on the closed nodes map
            closed_nodes_map[y][x] = 1

            # quit searching when the goal state is reached
            # if n0.estimate(xFinish, yFinish) == 0:
            if x == xFinish and y == yFinish:
                # generate the path from finish to start
                # by following the directions
                path = ''
                while not (x == xStart and y == yStart):
                    j = dir_map[y][x]
                    c = str((j + directions / 2) % directions)
                    path = str(c) + path
                    x += dx[j]
                    y += dy[j]

                rpath = []
                for e in path:
                    rpath.append((dx[int(e)], dy[int(e)]))

                return rpath

            # generate moves (child nodes) in all possible directions
            for i in range(directions):
                xdx = x + dx[i]
                ydy = y + dy[i]

                if not (xdx < 0 or xdx > n-1 or ydy < 0 or ydy > m - 1 or the_map[ydy][xdx] == 1 or
                        closed_nodes_map[ydy][xdx] == 1):
                    # generate a child node

                    m0 = node(xdx, ydy, n0.distance, n0.priority)

                    m0.nextdistance(i)
                    m0.updatePriority(xFinish, yFinish)

                    # if it is not in the open list then add into that
                    if open_nodes_map[ydy][xdx] == 0:
                        open_nodes_map[ydy][xdx] = m0.priority
                        heappush(pq[pqi], m0)
                        # mark its parent node direction
                        dir_map[ydy][xdx] = (i + directions / 2) % directions
                    elif open_nodes_map[ydy][xdx] > m0.priority:
                        # update the priority info
                        open_nodes_map[ydy][xdx] = m0.priority
                        # update the parent direction info
                        dir_map[ydy][xdx] = (i + directions / 2) % directions
                        # replace the node
                        # by emptying one pq to the other one
                        # except the node to be replaced will be ignored
                        # and the new node will be pushed in instead
                        while not (pq[pqi][0].xPos == xdx and pq[pqi][0].yPos == ydy):
                            heappush(pq[1 - pqi], pq[pqi][0])
                            heappop(pq[pqi])
                        heappop(pq[pqi]) # remove the wanted node
                        # empty the larger size pq to the smaller one
                        if len(pq[pqi]) > len(pq[1 - pqi]):
                            pqi = 1 - pqi
                        while len(pq[pqi]) > 0:
                            heappush(pq[1-pqi], pq[pqi][0])
                            heappop(pq[pqi])
                        pqi = 1 - pqi
                        heappush(pq[pqi], m0) # add the better node instead
        return []  # no route

    def get_path(self, (x0, y0), (x1, y1)):
        directions = 8
        dx = [1, 1, 0, -1, -1, -1, +0, +1]
        dy = [0, 1, 1, +1, +0, -1, -1, -1]

        the_invert_map = self.parent.game_data.places_truly_empty  # [[0]*100 for d in range(100)]  #
        # for y in range(100):
        #     for x in range(100):
        #         if the_invert_map[y][x] =

        the_map = [[0 if the_invert_map[uy][ux] else 1 for ux in range(100)] for uy in range(100)]

        route = self.pathFind(the_map, directions, dx, dy, x0, y0, x1, y1)
        return route