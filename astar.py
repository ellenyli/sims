import math
import heapq
from scipy.spatial import distance as dst
import time_path

# priority queue class using heapq library
class PriorityQueue:
    def __init__(self):
        self.elements = []
    
    def empty(self):
        return len(self.elements) == 0
    
    def put(self, item, priority):
        heapq.heappush(self.elements, (priority, item))
    
    def get(self):
        return heapq.heappop(self.elements)[1]

# calculates Manhattan distance between two points
def manhattan (p1, p2):
	(x1, y1), (x2, y2) = p1, p2
	return math.fabs(x1 - x2) + math.fabs(y1 - y2)

# returns list of heuristic distances between nodes and ending node
# variable end is an index representing the ending node
def heuristic (nodes, end):
	lst = []
	for i in range(len(nodes)):
		lst.append(manhattan(nodes[i], nodes[end])) 
	return lst

# from a dict, reconstructs path from start to end
# start, end: indices of starting and ending nodes
# came_from: dict of individual paths
def reconstruct_path(came_from, start, end):
	current = end
	path = [end]
	while current != start:
		current = came_from[current]
		path.append(current)
	path.reverse()
	return path

# checks if three points are collinear
def collinear (x, y, z):
	first = int(x[0]) == int(y[0]) and int(y[0]) == int(z[0])
	second = int(x[1]) == int(y[1]) and int(y[1]) == int(z[1])
	return (first or second)

# calculates number of turns in a path
def turns (came_from, lst, current, succ, start):
	came_from[succ] = current
	path = reconstruct_path (came_from, start, succ)
	shortened = [path[0]]
	for i in range(1, len(path) - 1):
		loc1, loc2, loc3 = lst[path[i-1]], lst[path[i]], lst[path[i+1]]
		if not collinear (loc1, loc2, loc3):
			shortened.append(path[i])
	shortened.append(path[len(path)-1])
	return len(shortened) - 2

# checks if x and y are within 500 inches of each other
def near (x, y):
	d = dst.euclidean(x, y)
	if d < 500:
		return 5 - (d // 100)
	else:
		return 0

# n: location of node, (x,y)
# d: list of door locations
def doors (n, d):
	cost_doors = 0
	for elt in d:
		cost_doors = cost_doors + near (n, elt)
	return cost_doors

# A* algorithm
# lst: list of dicts for each node, containing name and location
# start, end: indices in lst for the starting and ending nodes
# g: graph of nodes with weighted edges, names of nodes in graph are 
# 	 indexes of nodes turned into strings
def astar (start, end, g, lst):
	frontier = PriorityQueue()
	h = heuristic (lst, end)
	frontier.put(start, h[start])
	came_from = {}
	cost_so_far = {}
	visited = []
	came_from[start] = None
	cost_so_far[start] = h[start]

	while not frontier.empty():
		current = frontier.get()

		if current == end:
			break

		for succ in g[current]:
			if succ in visited:
				continue
			visited.append(succ)
			dist_cost = cost_so_far[current] + h[succ] - h[current] + g[current][succ]["weight"]
			turn_cost = turns (came_from, lst, current, succ, start) * 100
			door_cost = doors (lst[succ], [lst[1], lst[2], lst[3], lst[4]]) * 50
			new_cost = dist_cost + turn_cost + door_cost
			if succ not in cost_so_far or new_cost < cost_so_far[succ]:
				cost_so_far[succ] = new_cost
				priority = new_cost
				frontier.put(succ, priority)
				came_from[succ] = current
	return (came_from, cost_so_far)

