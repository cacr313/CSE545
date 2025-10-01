import math
import tkinter as tk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def create_distance_matrix(filename):
    coords = [] # empty array for (x, y) coordinates

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
    return coords


def euclidean(a, b):

    # distance between point a and b
    return math.hypot(a[0] - b[0], a[1] - b[1])

# find shortest distance from point p to line segment ab
def point_segment_distance(p, a, b):
    ax, ay = a; bx, by = b; px, py = p 
    vx, vy = bx - ax, by - ay # vector along segment ab
    wx, wy = px - ax, py - ay # vector from ab to p
    seg_len2 = vx*vx + vy*vy # squared lenght of vector of ab
   
    if seg_len2 == 0: # if the segment is a point
        return math.hypot(px-ax, py-ay), 0.0 # find hypotenuse
    
    t = (vx*wx + vy*wy) / seg_len2 # projects w onto v
    
    if t < 0.0: # closest point is before the segment
        return math.hypot(px-ax, py-ay), 0.0
   
    elif t > 1.0: # closest point is after the segment
        return math.hypot(px-bx, py-by), 1.0
    
    # closest point is on the segment
    projx = ax + t * vx
    projy = ay + t * vy

    return math.hypot(px-projx, py-projy), t 

# total distance of the tour 
def tour_length(coords, tour):
    total = 0.0
    n = len(tour)
    for i in range(n):
        total += euclidean(coords[tour[i]], coords[tour[(i+1) % n]])
    return total

# GUI 

class ClosestEdgeGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Traveling Sales Person Insertion")

        # variables
        self.coords = []
        self.tour = []
        self.remaining = set()
        self.history = []

        # Matplotlib Figure
        self.fig, self.ax = plt.subplots(figsize=(6, 6))
        self.canvas = FigureCanvasTkAgg(self.fig, master=root)
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        # buttons
        frame = tk.Frame(root)
        frame.pack(side=tk.BOTTOM, fill=tk.X)
        
        # load random30.tsp
        self.load30_btn = tk.Button(frame, text="Load Random30", command=lambda: self.load_file("Random30.tsp"))
        self.load30_btn.pack(side=tk.LEFT, padx=5, pady=5)

        # load random40.tsp
        self.load40_btn = tk.Button(frame, text="Load Random40", command=lambda: self.load_file("Random40.tsp"))
        self.load40_btn.pack(side=tk.LEFT, padx=5, pady=5)

        # starts with beginning and ending points
        self.start_btn = tk.Button(frame, text="Start", command=self.start_algo, state=tk.DISABLED)
        self.start_btn.pack(side=tk.LEFT, padx=5, pady=5)

        # walk through path 
        self.step_btn = tk.Button(frame, text="Step", command=self.step_algo, state=tk.DISABLED)
        self.step_btn.pack(side=tk.LEFT, padx=5, pady=5)

        # directions
        self.info_label = tk.Label(frame, text="Choose a dataset to begin.")
        self.info_label.pack(side=tk.LEFT, padx=10)

        # route
        self.route_label = tk.Label(frame, text="Current route: []", anchor='w')
        self.route_label.pack(fill=tk.X, padx=5)

        # distance 
        self.distance_label = tk.Label(frame, text="Current distance: 0.00", anchor='w')
        self.distance_label.pack(fill=tk.X, padx=5)

    def load_file(self, filename):
        self.coords = create_distance_matrix(filename) # load coordinates from selected file

        self.ax.clear() # clear previous plot 
        
        xs, ys = zip(*self.coords) # create x and y coords for plotting
        self.ax.scatter(xs, ys, color="darkmagenta")
        
        # label city numbers 
        for i, (x, y) in enumerate(self.coords):
            self.ax.text(x, y, str(i+1), fontsize=8, ha='right')
        
        self.ax.set_title(filename)
        self.ax.set_aspect('equal')
        self.canvas.draw()
        
        # enable start button
        self.start_btn.config(state=tk.NORMAL)
        self.info_label.config(text=f"Loaded {len(self.coords)} cities from {filename}")
        
        # reset variables
        self.tour = []
        self.remaining = set()
        self.history = []
        self.route_label.config(text="Current route: []")
        self.distance_label.config(text="Current distance: 0.00")
    
     # start the tour with the two cities closest to x=0
    def start_algo(self):
        # sort cities by distance from y=0 (closest to x-axis)
        sorted_by_y = sorted(range(len(self.coords)), key=lambda i: abs(self.coords[i][1]))

    # take the first two (closest to x=0)
        candidates = sorted_by_y[:5]  # take a few in case of ties
        best = None
        for i in range(len(candidates)): 
            for j in range(i+1, len(candidates)):
                d = euclidean(self.coords[candidates[i]], self.coords[candidates[j]])
                if best is None or d < best[0]:
                    best = (d, candidates[i], candidates[j])

        _, a, b = best
        self.tour = [a, b] # initial tour
        self.remaining = set(range(len(self.coords))) - {a, b} # remaining cities
        self.history = [a, b]

        self.update_plot() # plot the initial tour
        self.step_btn.config(state=tk.NORMAL)
        cost = tour_length(self.coords, self.tour)
        self.info_label.config(text=f"Started with cities {a+1} and {b+1}")
        self.route_label.config(text=f"Current route: {[i+1 for i in self.tour]}")
        self.distance_label.config(text=f"Current distance: {cost:.2f}")

    # insert next city using closest edge insertion heuristic
    def step_algo(self):
        if not self.remaining: # if no cities remain end tour
            self.info_label.config(text="Tour complete!")
            return

        candidate_best = {} # empty diction to store best edge for each remaining city 
        for v in list(self.remaining): # loop remaining cities
           
           # initilize variables
            best_d = None
            best_edge_idx = None
           
            m = len(self.tour) # number of cities currently in the tour

            # loop over each edge in the tour
            for ei in range(m):
                u = self.tour[ei] # start of edge
                w = self.tour[(ei+1) % m] # end of edge
                d, _ = point_segment_distance(self.coords[v], self.coords[u], self.coords[w]) # distance from city v to edge connecting u and w
                
                # keep track of best variables
                if best_d is None or d < best_d:
                    best_d = d
                    best_edge_idx = ei
            candidate_best[v] = (best_d, best_edge_idx) #store best variables in candidate_best for city v

        v_star = min(candidate_best.items(), key=lambda kv: kv[1][0])[0] # select the city to insert next
        best_edge_idx = candidate_best[v_star][1] # find the index of the edge where v_star should be inserted
        insert_pos = best_edge_idx + 1 # position on tour list 
        
        # add v_star and remove from remaining cities
        self.tour.insert(insert_pos, v_star) 
        self.remaining.remove(v_star)
        self.history.append(v_star)

        # update the plot with new city
        self.update_plot()
        cost = tour_length(self.coords, self.tour)
        self.info_label.config(text=f"Inserted {v_star+1}")
        self.route_label.config(text=f"Current route: {[i+1 for i in self.tour]}")
        self.distance_label.config(text=f"Current distance: {cost:.2f}")

    def update_plot(self):

        self.ax.clear()
        xs,ys = zip(*self.coords)
        self.ax.scatter(xs, ys, color="darkmagenta")
        
        for i, (x, y) in enumerate(self.coords):
            self.ax.text(x, y, str(i+1), fontsize=8, ha='right')
        
        # plot tour edges
        if self.tour:
            tour_x = [self.coords[i][0] for i in self.tour] + [self.coords[self.tour[0]][0]]
            tour_y = [self.coords[i][1] for i in self.tour] + [self.coords[self.tour[0]][1]]
            self.ax.plot(tour_x, tour_y, color="pink")
        
        self.ax.set_title("Closest Edge Insertion")
        self.ax.set_aspect('equal')
        self.canvas.draw()

# Run GUI
if __name__ == "__main__":
    root = tk.Tk()
    app = ClosestEdgeGUI(root)
    root.mainloop()

