import math   # used for distance formula
import time  # used for timing computation time
from collections import deque  # for BFS queue

def create_distance_matrix(filename):
    coords = []  # empty array for (x, y) coordinates

    # opens file and reads each line
    with open(filename, 'r') as f:
        lines = f.readlines()

    reading_coords = False # used to know when to start recording coordinates

    for line in lines: # read each line
        line = line.strip() # remove whitespace

        # set reading_coords to true when hitting the node section
        if line.startswith("NODE_COORD_SECTION"):
            reading_coords = True
            continue

        #record coordinates until it gets to the end of the file
        if reading_coords:
            if line == "" or line.startswith("EOF"):
                break
            x, y = line.split()[1:] # start at x coordinate
            coords.append((float(x), float(y)))

    #create empty matrix for n amount of cities
    n = len(coords)
    matrix = [[0] * n for _ in range(n)]

    # fills in matrix using distance formula
    for i in range(n):
        for j in range(n):
            if i != j: # do not calculate distance for traveling to the same city
                x = coords[i][0] - coords[j][0]
                y = coords[i][1] - coords[j][1]
                dist = math.sqrt(x**2 + y**2)
                matrix[i][j] = dist
    return matrix


# add distances together for each matrix row
def calculate_path_distance(matrix, path):
    dist = 0
    for i in range(len(path) - 1):
        # subtract 1 for matrix indexing
        dist += matrix[path[i] - 1][path[i + 1] - 1]
    return dist


# BFS Search
def bfs(graph, start, goal):
    # initialize the queue with the current node and path taken
    queue = deque([(start, [start])])
    visited_count = 0

    # contiune until end city is visited
    while queue:

        # FIFO for BFS and count as visited
        current, path = queue.popleft()
        visited_count += 1

        # stop if the end city is visited
        if current == goal:
            return path, visited_count

        # travel in numberical order
        for neighbor in sorted(graph[current]): 

            # add city to path if not a repeat 
            if neighbor not in path:
                queue.append((neighbor, path + [neighbor]))

    # if no path, return
    return None, visited_count


# DFS Search
def dfs(graph, start, goal, path=None, visited_count=None):
    
    # initialize path on the first call
    if path is None:
        path = []

    # initialize list for visited node
    if visited_count is None:
        visited_count = [0] # needs to be a list since it is recursive

    # start at the start city
    path = path + [start]
    visited_count[0] += 1

    # stop at the end city
    if start == goal:
        return path, visited_count[0]

    # travel in numerical order 
    for neighbor in sorted(graph[start]):

        # if city is not already in the path, recursively call DFS with neighbor as the new start
        if neighbor not in path:
            new_path, _ = dfs(graph, neighbor, goal, path, visited_count)

            # if valid path, return it 
            if new_path:
                return new_path, visited_count[0]

    # if no path, return
    return None, visited_count[0]



if __name__ == "__main__":
    tsp_file = "11PointDFSBFS.tsp"  

    #creat the distance matrix for the given file  
    matrix = create_distance_matrix(tsp_file)

    # connected edjes table
    graph = {
        1: [2, 3, 4],
        2: [3],
        3: [4, 5],
        4: [5, 6, 7],
        5: [7, 8],
        6: [8],
        7: [9, 10],
        8: [9, 10, 11],
        9: [11],
        10: [11],
        11: []
    }

    start_city = 1
    goal_city = 11

    # BFS 
    start_time = time.time()
    bfs_path, bfs_cities = bfs(graph, start_city, goal_city)
    bfs_time = time.time() - start_time
    bfs_cost = calculate_path_distance(matrix, bfs_path)

    # DFS 
    start_time = time.time()
    dfs_path, dfs_cities = dfs(graph, start_city, goal_city)
    dfs_time = time.time() - start_time
    dfs_cost = calculate_path_distance(matrix, dfs_path)

    # Print Results 
    print("BFS Results:")
    print(f"Path: {bfs_path}")
    print(f"Total distance: {bfs_cost:.2f}")
    print(f"Cities Visited: {bfs_cities}")
    print(f"Run-Time: {bfs_time:.6f} seconds\n")

    print("DFS Results:")
    print(f"Path: {dfs_path}")
    print(f"Total distance: {dfs_cost:.2f}")
    print(f"Cities Visited: {dfs_cities}")
    print(f"Run-Time: {dfs_time:.6f} seconds")
