import itertools # used for generating permutations for every path
import math # used for distance formula
import time # used for timing computation time

def create_distance_matrix(filename):
    coords = [] # empty array for (x,y) coordinates

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

        # record coordinates until it gets to the end of the file 
        if reading_coords:
            if line == "":
                break
            x, y = line.split()[1:] # start at x coordinate
            coords.append((float(x), float(y))) 
    
    # create empty matrix for n amount of cities 
    n = len(coords)
    matrix = [[0]*n for _ in range(n)]
    
    # fills in matrix using distance formula
    for i in range(n):
        for j in range(n): 
            if i != j: # do not calculate distance for traveling to the same city
                x = coords[i][0] - coords[j][0]
                y = coords[i][1] - coords[j][1]
                dist = (math.sqrt(x**2 + y**2)) 
                matrix[i][j] = dist
    return matrix


# add distances together for each matrix row
def calculate_path_distance(matrix, path):
    dist = 0
    for i in range(len(path) - 1):
        dist += matrix[path[i]][path[i + 1]] # add distance from one city to another 
    dist += matrix[path[-1]][path[0]] # add distance to return to starting city
    return dist


def brute_force_tsp(matrix):

    # create a list of all cities
    n = len(matrix)
    cities = list(range(n))

    # initialize variables for finding shortest path
    shortest_distance = float("inf")
    best_path = None

    start_city = cities[0]
    other_cities = cities[1:] # exclude the starting city

    # permutation for every possible ordering of the cities
    for perm in itertools.permutations(other_cities):
        path = [start_city] + list(perm)
        distance = calculate_path_distance(matrix, path) # calculate the distance for that permutation

        #set shortest_distance and best_path if less than previous shortest_distance
        if distance < shortest_distance: 
            shortest_distance = distance    
            best_path = path

    return shortest_distance, best_path


if __name__ == "__main__":
    tsp_file = "Random12.tsp"   

    # create the distance matrix for the given file
    matrix = create_distance_matrix(tsp_file)
    start_time = time.time() # start timer

    # perform brute force approach to the calculated matrix 
    shortest_distance, best_path = brute_force_tsp(matrix)

    # end timer
    end_time = time.time()
    total_time = end_time - start_time

    # print results
    print("Minimum Cost Path:")

    # add 1 for correct city numbering in file and add starting city to the end for full path
    print("Path:", [p+1 for p in best_path] + [best_path[0]+1])  
    print(f"Cost: {shortest_distance: .2f}")
    print(f"Run-Time: {total_time: .2f}  seconds")

