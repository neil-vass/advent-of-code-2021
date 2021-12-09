import math

class Floor:
    def __init__(self, data):
        self.heightmap = data

    def neighbours_of(self, x, y):
        neighbours = set()
        if x > 0:
            neighbours.add((x-1, y))    
        if y > 0:
            neighbours.add((x, y-1))
        if x < (len(self.heightmap) - 1):
            neighbours.add((x+1, y))
        if y < (len(self.heightmap[x]) - 1):
            neighbours.add((x, y+1))

        return neighbours
        
    def is_low_point(self, x, y):
        value = self.heightmap[x][y]
        return all((value < self.heightmap[xn][yn]) for xn, yn in self.neighbours_of(x, y))

    def find_low_points(self):
        low_points = set()
        for x in range(len(self.heightmap)):
            for y in range(len(self.heightmap[x])):
                if self.is_low_point(x, y):
                    low_points.add((x, y))
        return low_points

    def sum_of_risks(self):
        return sum([(self.heightmap[x][y] + 1) for x, y in self.find_low_points()])


    def find_basin_for(self, x, y, basin_so_far=None):
        if basin_so_far is None:
            basin_so_far = {(x,y)}

        for xn, yn in self.neighbours_of(x, y):
            if (xn, yn) not in basin_so_far and self.heightmap[xn][yn] < 9:
                basin_so_far.add((xn,yn))
                basin_so_far |= self.find_basin_for(xn, yn, basin_so_far)

        return basin_so_far

    def find_basin_sizes(self):
        return [len(self.find_basin_for(*p)) for p in self.find_low_points()]

    def multiply_3_largest_basins(self):
        basins = self.find_basin_sizes()
        return math.prod(sorted(basins)[-3:])

def fetch_data(path):
    data = []
    with open(path, 'r') as f:
        for ln in f:
            data.append([int(n) for n in ln.rstrip()])
    return data

#--------------------- tests -------------------------#

def test_fetch_data():
    data = fetch_data('sample_data/day09.txt')
    assert len(data) == 5
    assert len(data[0]) == 10
    assert data[1][1] == 9

def test_floor_finds_neighbours():
    data = fetch_data('sample_data/day09.txt')
    floor = Floor(data)
    assert floor.neighbours_of(0, 0) == {(0,1), (1,0)}
    assert floor.neighbours_of(1, 1) == {(0,1), (1,0), (1,2), (2,1)}
    assert floor.neighbours_of(4, 2) == {(3,2), (4,1), (4,3)}

def test_floor_finds_low_points():
    data = fetch_data('sample_data/day09.txt')
    floor = Floor(data)
    assert floor.find_low_points() == {(0,1), (0,9), (2,2), (4,6)}

def test_sum_of_risks():
    data = fetch_data('sample_data/day09.txt')
    floor = Floor(data)
    assert floor.sum_of_risks() == 15

def test_find_basin_for():
    data = fetch_data('sample_data/day09.txt')
    floor = Floor(data)
    assert floor.find_basin_for(0, 1) == {(0,1), (0,0), (1,0)}

def test_find_basin_sizes():
    data = fetch_data('sample_data/day09.txt')
    floor = Floor(data)
    basin_sizes = floor.find_basin_sizes()
    # Want the right results, don't care about order.
    assert len(basin_sizes) == 4
    assert set(basin_sizes) == set([3, 9, 14, 9])

def test_multiply_3_largest_basins():
    data = fetch_data('sample_data/day09.txt')
    floor = Floor(data)
    assert floor.multiply_3_largest_basins() == 1134

#-----------------------------------------------------#

if __name__ == "__main__":
    data = fetch_data('data/day09.txt')
    floor = Floor(data)
    print(floor.multiply_3_largest_basins())
   
