# Really no need for numpy but I like practicing with it.
import numpy as np

class Octo:
    def __init__(self, lines):
        self.grid = np.array([[int(d) for d in ln] for ln in lines])

    def increment_point_and_neighbours(self, x, y):
        for xn in (x-1, x, x+1):
            for yn in (y-1, y, y+1):
                if (0 <= xn < self.grid.shape[0]) and (0 <= yn < self.grid.shape[1]):
                    self.grid[xn,yn] += 1

    def step(self):
        self.grid += 1

        already_flashed = []
        flashes = np.argwhere(self.grid > 9)
        while len(flashes):
            for x, y in flashes:
                self.increment_point_and_neighbours(x, y)
                already_flashed.append([x,y])
            flashes = [p for p in np.argwhere(self.grid > 9).tolist() if p not in already_flashed]
        
        self.grid[self.grid > 9] = 0
                

    def get_flash_count(self, steps):
        count = 0
        for _ in range(steps):
            self.step()
            count += np.count_nonzero(self.grid == 0)
        return count

    def step_to_synchro_flash(self):
        steps = 0
        while np.count_nonzero(self.grid == 0) != self.grid.size:
            self.step()
            steps += 1
        return steps

def fetch_data(path):
    with open(path, 'r') as f:
        for ln in f:
            yield ln.rstrip()

#--------------------- tests -------------------------#

def test_octo_init():
    lines = [
        '11111',
        '19991',
        '19191',
        '19991',
        '11111'
    ]
    octo = Octo(lines)
    assert octo.grid[0,0] == 1
    assert octo.grid[1,1] == 9

def test_step():
    lines = [
        '11111',
        '19991',
        '19191',
        '19991',
        '11111'
    ]
    octo = Octo(lines)
    octo.step()

    assert octo.grid[0,0] == 3
    assert octo.grid[1,1] == 0
    assert octo.grid[2,2] == 0

def test_step_with_sample_data():
    data = fetch_data('sample_data/day11.txt')
    octo = Octo(data)
    octo.step()
    assert octo.grid[0,0] == 6
    assert octo.grid[1,1] == 8
    assert np.count_nonzero(octo.grid == 0) == 0
    octo.step()
    assert octo.grid[0,0] == 8
    assert octo.grid[1,1] == 0
    assert np.count_nonzero(octo.grid == 0) == 35

def test_get_flash_count():
    data = fetch_data('sample_data/day11.txt')
    octo = Octo(data)
    assert octo.get_flash_count(steps=100) == 1656

def test_step_to_synchro_flash():
    data = fetch_data('sample_data/day11.txt')
    octo = Octo(data)
    assert octo.step_to_synchro_flash() == 195
#-----------------------------------------------------#

if __name__ == "__main__":
    data = fetch_data('data/day11.txt')
    octo = Octo(data)
    print(octo.step_to_synchro_flash())
