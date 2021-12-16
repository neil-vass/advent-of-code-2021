import numpy as np
import numpy.ma as ma
import heapq

# Class adds to heapq, following advice from 
# https://docs.python.org/3/library/heapq.html#priority-queue-implementation-notes
class PriorityQueue:
    REMOVED = '<removed-item>'

    def __init__(self):
        self._queue = []
        self._lookup = {}

    def push(self, x, y, val):
        entry = [val, (x,y)]
        heapq.heappush(self._queue, entry)
        self._lookup[(x,y)] = entry

    def update(self, x, y, newval):
        if (x,y) in self._lookup:
            self._lookup[(x,y)][1] = self.REMOVED
        self.push(x, y, newval)

    def pop(self):
        while self._queue:
            entry = heapq.heappop(self._queue)
            if entry[1] != self.REMOVED:
                val, (x,y) = entry
                del self._lookup[(x,y)]
                return x, y
        raise KeyError('pop from empty priority queue')

        

def fetch_data(path):
    with open(path, 'r') as f:
        return np.array([[int(d) for d in ln.rstrip()] for ln in f])


# No longer used: horribly inefficient way to find the next node to use.
# Now managed with a priority queue.
def lowest_distance_unvisited_node(arr):
    candidates = np.where(arr == arr.min())
    return candidates[0][0], candidates[1][0]


def unvisited_neighbours(arr, x, y):
    neighbours = []
    if x > 0 and arr[x-1, y] is not ma.masked:
        neighbours.append((x-1, y))
    if x < arr.shape[0]-1 and arr[x+1, y] is not ma.masked:
        neighbours.append((x+1, y))
    if y > 0 and arr[x, y-1] is not ma.masked:
        neighbours.append((x, y-1))
    if y < arr.shape[1]-1 and arr[x, y+1] is not ma.masked:
        neighbours.append((x, y+1))
    return neighbours


# Find the lowest risk path from [0,0] to [-1,-1] (we can make those params later if needed).
# Uses Dijkstra's algorithm (https://en.wikipedia.org/wiki/Dijkstra%27s_algorithm#Algorithm), 
# and returns the sum of risks along the chosen path.
def find_lowest_risk_path(risks):
    # Array same size as "risks", set distances to "infinity" and everything unvisited.
    # Use a masked array - we'll mask entries as they get visited.
    tentative_distances = ma.empty_like(risks)
    tentative_distances.fill(999999999)

    # Distance from start point to itself is 0. 
    tentative_distances[0,0] = 0

    nodes_to_visit = PriorityQueue()
    nodes_to_visit.push(0,0,0)

    while not tentative_distances.mask.all():
        current_x, current_y = nodes_to_visit.pop()
        
        for xn, yn in unvisited_neighbours(tentative_distances, current_x, current_y):
            distance = tentative_distances[current_x, current_y] + risks[xn, yn]
            if tentative_distances[xn, yn] > distance:
                tentative_distances[xn, yn] = distance
                nodes_to_visit.update(xn, yn, distance)
        
        # Done with current node, mark it as visited.
        tentative_distances[current_x, current_y] = ma.masked

    # Done! The exit node will have the shortest path (lowest sum of risks)
    tentative_distances.mask = ma.nomask
    return tentative_distances[-1,-1]


def expand_map(risks, scale=5):
    risks_x_size, risks_y_size = risks.shape
    more_risks = np.empty(shape=(risks_x_size * scale, risks_y_size * scale), dtype=np.int64)

    # Copy the risks across, incrementing all numbers to position of the copy - but don't do the wraparound yet.
    for x_inc in range(scale):
        for y_inc in range(scale):
            x_start = x_inc * risks_x_size
            x_end = x_start + risks_x_size
            y_start = y_inc * risks_y_size
            y_end = y_start + risks_y_size
            more_risks[x_start:x_end, y_start:y_end] = (risks + (x_inc + y_inc))

    # Wrap around all figures (if incremented past 9, go back to 1 and carry on).
    more_risks = ((more_risks-1) % 9) + 1

    return more_risks

#--------------------- tests -------------------------#

def test_fetch_data():
    risks = fetch_data('sample_data/day15.txt')
    assert risks.shape == (10,10)
    assert risks[1,2] == 8

def test_find_lowest_risk_path():
    risks = fetch_data('sample_data/day15.txt')
    assert find_lowest_risk_path(risks) == 40

def test_expand_map():
    risks = fetch_data('sample_data/day15.txt')
    more_risks = expand_map(risks)
    assert more_risks.shape == (50, 50)
    assert more_risks[0,0] == 1
    assert more_risks[0,-1] == 6
    assert more_risks[7,-1] == 4
    assert more_risks[-1,-1] == 9

def test_find_lowest_risk_path_in_expanded_map():
    risks = fetch_data('sample_data/day15.txt')
    more_risks = expand_map(risks)
    assert find_lowest_risk_path(more_risks) == 315


# Initial version (using my lowest_distance_unvisited_node function)
# took 6 minutes to complete. Changed to use a priority queue and that 
# dropped to 6 seconds. There's a lesson here!
def test_find_lowest_risk_path_with_actual_puzzle_input():
    risks = fetch_data('data/day15.txt')
    more_risks = expand_map(risks)
    assert find_lowest_risk_path(more_risks) == 2858


#-----------------------------------------------------#

if __name__ == "__main__":
    risks = fetch_data('data/day15.txt')
    more_risks = expand_map(risks)
    print(find_lowest_risk_path(more_risks))
