# search.py
# ---------------
# Licensing Information:  You are free to use or extend this projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to the University of Illinois at Urbana-Champaign
#
# Created by Michael Abir (abir2@illinois.edu) on 08/28/2018

"""
This is the main entry point for MP1. You should only modify code
within this file -- the unrevised staff files will be used for all other
files and classes when code is run, so be careful to not modify anything else.
"""

from queue import PriorityQueue

# Search should return the path.
# The path should be a list of tuples in the form (row, col) that correspond
# to the positions of the path taken by your search algorithm.
# maze is a Maze object based on the maze from the file specified by input filename
# searchMethod is the search method specified by --method flag (bfs,dfs,astar,astar_multi,extra)

def search(maze, searchMethod):
    return {
        "bfs": bfs,
        "astar": astar,
        "astar_corner": astar_corner,
        "astar_multi": astar_multi,
        "extra": extra,
    }.get(searchMethod)(maze)


def bfs(maze):
    """
    Runs BFS for part 1 of the assignment.

    @param maze: The maze to execute the search on.

    @return path: a list of tuples containing the coordinates of each state in the computed path
    """
    # TODO: Write your code here
    frontier = []
    visited = []
    ans = []
    path = {}
    x_start, y_start = maze.getStart()
    end = maze.getObjectives()
    x_end, y_end = end.pop(0)
    frontier.append((x_start, y_start))
    path[x_start, y_start] = x_start, y_start
    finish = False

    while len(frontier) > 0 and finish == False:
        x, y = frontier.pop(0)
        canVisit = maze.getNeighbors(x, y)
        while len(canVisit) > 0:
            x_move, y_move = canVisit.pop(0)
            movement = (x_move, y_move)
            if maze.isValidMove(x_move, y_move) and movement not in visited:
                path[movement] = x, y
                frontier.append(movement)
                visited.append(movement)
            if movement == (x_end, y_end):
                finish = True

    x, y = x_end, y_end
    while (x, y) != (x_start, y_start):
        ans.insert(0, (x, y))
        x, y = path[x, y]

    ans.insert(0, (x_start, y_start))

    return ans


def astar(maze):
    """
    Runs A star for part 1 of the assignment.

    @param maze: The maze to execute the search on.

    @return path: a list of tuples containing the coordinates of each state in the computed path
    """
    # TODO: Write your code here
    frontier, visited, ans = [], [], []
    path = {}
    g, h, f = {}, {}, {}
    x_start, y_start = maze.getStart()
    end = maze.getObjectives()
    x_end, y_end = end.pop(0)
    frontier.append((x_start, y_start))
    path[x_start, y_start] = x_start, y_start
    g[x_start, y_start], h[x_start, y_start], f[x_start, y_start] = 0, 0, 0
    finish = False

    while len(frontier) > 0 and finish == False:
        # print(frontier)
        x, y = frontier[0]
        i = 0
        for index, node in enumerate(frontier):
            if f[node] < f[x, y]:
                x, y = node
                i = index
        visited.append((x, y))
        frontier.pop(i)
        canVisit = maze.getNeighbors(x, y)
        while len(canVisit) > 0:
            x_move, y_move = canVisit.pop(0)
            movement = (x_move, y_move)
            if maze.isValidMove(x_move, y_move) and movement not in visited and movement not in frontier:
                path[movement] = x, y
                if x_move == x_end and y_move == y_end:
                    finish = True
                    break
                frontier.append(movement)
                g[movement] = g[x, y] + 1
                h[movement] = ((x_move - x_end) ** 2 + (y_move - y_end) ** 2) ** 0.5
                f[movement] = g[movement] + h[movement]
        if finish == True:
            break

    x, y = x_end, y_end
    while (x, y) != (x_start, y_start):
        ans.insert(0, (x, y))
        x, y = path[x, y]

    ans.insert(0, (x_start, y_start))

    return ans


def astar_corner(maze):
    """
    Runs A star for part 2 of the assignment in the case where there are four corner objectives.
        
    @param maze: The maze to execute the search on.
        
    @return path: a list of tuples containing the coordinates of each state in the computed path
        """

    # TODO: Write your code here

    def getLength(path, step):
        returnPath = []
        for x in path[(step[0], step[1])]:
            returnPath.append(x)
        for i in range(1, 4):
            temp = []
            if step[i] > step[i + 1]:
                for x in path[(step[i + 1], step[i])]:
                    temp.append(x)
                temp.reverse()
                temp.pop(0)
                returnPath += temp
            else:
                for x in path[(step[i], step[i + 1])]:
                    temp.append(x)
                temp.pop(0)
                returnPath += temp
        return returnPath

    x_start, y_start = maze.getStart()
    points = maze.getObjectives()
    points.insert(0, (x_start, y_start))
    path = {}
    ans, tempList, path_step = [], [], [0, 1, 2, 3, 4]

    for i in range(4):
        j = i + 1
        while j < 5:
            path[(i, j)] = getPath_astar(maze, points[i], points[j])
            # path[(i, j)] = get_path(maze, points[i], points[j])
            j += 1
    ans = getLength(path, path_step)

    for i in range(1, 5):
        for x in range(1, 5):
            if x == i:
                continue
            for y in range(1, 5):
                if y == x or y == i:
                    continue
                for z in range(1, 5):
                    if z == y or z == x or z == i:
                        continue
                    path_step = [0, i, x, y, z]
                    tempList = getLength(path, path_step)
                    if len(ans) > len(tempList):
                        ans = tempList

    return ans


# return the shortest path from start point to end point by BFS
def getPath_bfs(maze, start_point, end_point):
    frontier = []
    visited = []
    ans = []
    path = {}
    x_start, y_start = start_point
    x_end, y_end = end_point
    frontier.append((x_start, y_start))
    path[x_start, y_start] = x_start, y_start
    finish = False

    while len(frontier) > 0 and finish is False:
        x, y = frontier.pop(0)
        canVisit = maze.getNeighbors(x, y)
        while len(canVisit) > 0:
            x_move, y_move = canVisit.pop(0)
            movement = (x_move, y_move)
            if maze.isValidMove(x_move, y_move) and movement not in visited:
                path[movement] = x, y
                frontier.append(movement)
                visited.append(movement)
            if movement == (x_end, y_end):
                finish = True

    x, y = x_end, y_end
    while (x, y) != (x_start, y_start):
        ans.insert(0, (x, y))
        x, y = path[x, y]

    ans.insert(0, (x_start, y_start))

    return ans


# return the shortest path from start point to end point by A*
def getPath_astar(maze, start_point, end_point):
    frontier = PriorityQueue()
    unvisited, visited, ans = [], [], []
    path = {}
    g, h, f = {}, {}, {}
    x_start, y_start = start_point
    x_end, y_end = end_point
    frontier.put((0, (x_start, y_start)))
    unvisited.append((x_start, y_start))
    path[x_start, y_start] = x_start, y_start
    g[x_start, y_start], h[x_start, y_start], f[x_start, y_start] = 0, 0, 0
    finish = False

    while frontier.qsize() > 0 and finish is False:
        d, position = frontier.get()
        x, y = position
        unvisited.remove((x, y))
        visited.append((x, y))
        canVisit = maze.getNeighbors(x, y)
        while len(canVisit) > 0:
            x_move, y_move = canVisit.pop(0)
            movement = (x_move, y_move)
            if maze.isValidMove(x_move, y_move) and movement not in visited and movement not in unvisited:
                path[movement] = x, y
                if x_move == x_end and y_move == y_end:
                    finish = True
                    break
                unvisited.append(movement)
                g[movement] = g[x, y] + 1
                h[movement] = ((x_move - x_end) ** 2 + (y_move - y_end) ** 2) ** 0.5
                f[movement] = g[movement] + h[movement]
                frontier.put((f[movement], movement))
        if finish is True:
            break

    x, y = x_end, y_end
    while (x, y) != (x_start, y_start):
        ans.insert(0, (x, y))
        x, y = path[x, y]

    ans.insert(0, (x_start, y_start))

    return ans

# class node
class Node:
    def __init__(self, x, y, g):
        self.x = x
        self.y = y
        self.g = g
        self.h = 0
        self.f = 0
        self.unvisited = []
        self.visited = []

    def __lt__(self, other):
        return self.f < other.f



def MST(distance, unvisited):
    h = 0
    if len(unvisited) < 1:
        return 0
    visited = [unvisited[0]]
    while len(visited) < len(unvisited):
        min_h = -1
        position = (0, 0)
        for point1 in visited:
            for point2 in unvisited:
                if point2 not in visited:
                    temp = distance[(point1, point2)] - 2
                    if min_h == -1 or min_h > temp:
                        min_h = temp
                        position = point2
        h += min_h
        visited.append(position)
    return h



def astar_multi(maze):
    """
    Runs A star for part 3 of the assignment in the case where there are
    multiple objectives.

    @param maze: The maze to execute the search on.

    @return path: a list of tuples containing the coordinates of each state in the computed path
    """
    # initialize
    points = maze.getObjectives()
    start_x, start_y = maze.getStart()
    points.insert(0, (start_x, start_y))
    path, distance, visited = {}, {}, []
    frontier = PriorityQueue()

    if len(points) == 0:
        return []
    if len(points) == 1:
        return getPath_astar(maze, (start_x, start_y), points[0])

    # get distances amount all the points
    for i in range(len(points)):
        j = i + 1
        while j < len(points):
            path[(points[i], points[j])] = getPath_astar(maze, points[i], points[j])
            temp_list = path[(points[i], points[j])].copy()
            temp_list.reverse()
            path[(points[j], points[i])] = temp_list
            distance[(points[i], points[j])] = len(path[(points[i], points[j])])
            distance[(points[j], points[i])] = len(path[(points[i], points[j])])
            j += 1

    # create start point node
    start_point = Node(start_x, start_y, 0)
    start_point.unvisited = points.copy()
    start_point.unvisited.pop(0)
    start_point.visited.append((start_x, start_y))
    frontier.put(start_point)
    end_point = Node(0, 0, 0)

    while frontier.qsize() > 0:
        current_point = frontier.get()
        if len(current_point.unvisited) == 0:
            end_point = current_point
            break
        for index, n in enumerate(current_point.unvisited):
            n_x, n_y = n
            next_point = Node(n_x, n_y, 0)
            next_point.unvisited = current_point.unvisited.copy()
            next_point.visited = current_point.visited.copy()
            next_point.unvisited.remove(n)
            next_point.visited.append((n_x, n_y))
            next_point.h = MST(distance, next_point.unvisited)
            next_point.g = current_point.g + distance[((current_point.x, current_point.y), n)] - 1
            next_point.f = next_point.h + next_point.g + len(next_point.unvisited)
            frontier.put(next_point)

    ans = [(start_x, start_y)]
    for index in range(len(end_point.visited) - 1):
        temp = path[(end_point.visited[index], end_point.visited[index+1])].copy()
        temp.pop(0)
        ans += temp
    return ans

def extra(maze):
    """
    Runs extra credit suggestion.

    @param maze: The maze to execute the search on.

    @return path: a list of tuples containing the coordinates of each state in the computed path
    """
    # TODO: Write your code here
    points = maze.getObjectives()
    start_x, start_y = maze.getStart()
    points.insert(0, (start_x, start_y))
    path, distance, visited = {}, {}, []

    # get distances amount all the points
    for i in range(len(points)):
        j = i + 1
        while j < len(points):
            path[(points[i], points[j])] = getPath_astar(maze, points[i], points[j])
            temp_list = path[(points[i], points[j])].copy()
            temp_list.reverse()
            path[(points[j], points[i])] = temp_list
            distance[(points[i], points[j])] = len(path[(points[i], points[j])])
            distance[(points[j], points[i])] = len(path[(points[i], points[j])])
            j += 1
    ans = [(start_x, start_y)]
    visited = get_path(distance, points)
    for index in range(len(visited) - 1):
        temp = path[(visited[index], visited[index + 1])].copy()
        temp.pop(0)
        ans += temp
    return ans

def get_path(distance, unvisited):
    h = 0
    if len(unvisited) < 1:
        return 0
    visited = [unvisited[0]]
    point1 = unvisited[0]
    while len(visited) < len(unvisited):
        min_d = -1
        position = (0, 0)
        for point2 in unvisited:
            if point2 not in visited:
                temp = distance[(point1, point2)]
                if min_d == -1 or min_d > temp:
                    min_d = temp
                    position = point2
        visited.append(position)
        point1 = position
    return visited
