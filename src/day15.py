import numpy as np
import numpy.ma as ma


def fetch_data(path):
    with open(path, 'r') as f:
        return np.array([[int(d) for d in ln.rstrip()] for ln in f])


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


# Find the lowest risk path from [0,0] to [-1,-1] (we can make those params later if needed)
# Uses Dijkstra's algorithm (https://en.wikipedia.org/wiki/Dijkstra%27s_algorithm#Algorithm), 
# and returns the sum of risks along the chosen path.
def find_lowest_risk_path(risks):
    # Array same size as "risks", set distances to "infinity" and everything unvisited.
    # Use a masked array - we'll mask entries as they get visited.
    tentative_distances = ma.empty_like(risks)
    tentative_distances.fill(999999999)

    # Distance from start point to itself is 0. 
    tentative_distances[0,0] = 0

    while not tentative_distances.mask.all():
        current_x, current_y = lowest_distance_unvisited_node(tentative_distances)
        
        for xn, yn in unvisited_neighbours(tentative_distances, current_x, current_y):
            distance = tentative_distances[current_x, current_y] + risks[xn, yn]
            if tentative_distances[xn, yn] > distance:
                tentative_distances[xn, yn] = distance
        
        # Done with current node, mark it as visited.
        tentative_distances[current_x, current_y] = ma.masked

    # Done! The exit node will have the shorted path (lowest sum of risks)
    tentative_distances.mask = ma.nomask
    return tentative_distances[-1,-1]

#--------------------- tests -------------------------#

def test_fetch_data():
    risks = fetch_data('sample_data/day15.txt')
    assert risks.shape == (10,10)
    assert risks[1,2] == 8

def test_find_lowest_risk_path():
    risks = fetch_data('sample_data/day15.txt')
    assert find_lowest_risk_path(risks) == 40
#-----------------------------------------------------#

if __name__ == "__main__":
    risks = fetch_data('data/day15.txt')
    print(find_lowest_risk_path(risks))
