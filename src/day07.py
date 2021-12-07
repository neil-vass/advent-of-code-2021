
def fetch_data(path):
    with open(path, 'r') as f:
        return [int(n) for n in f.readline().split(',')]

def align_on(positions, target):
    return sum(abs(p - target) for p in positions)

def find_cheapest_target(positions):
    costs = [(t, align_on(positions, t)) for t in set(positions)]
    return min(costs, key=lambda c: c[1])


def align_on_pt2(positions, target):
    cost = 0
    for p in positions:
        dist = abs(p - target)
        cost += (dist+1) * (dist/2)
    return int(cost)

def find_cheapest_target_pt2(positions):
    costs = [(t, align_on_pt2(positions, t)) for t in range(min(positions), max(positions)+1)]
    return min(costs, key=lambda c: c[1])

#--------------------- tests -------------------------#

def test_fetch_data():
    data = fetch_data('sample_data/day07.txt')
    assert data == [16,1,2,0,4,2,7,1,2,14]

def test_align_on():
    data = fetch_data('sample_data/day07.txt')
    assert align_on(data, 1) == 41
    assert align_on(data, 3) == 39
    assert align_on(data, 10) == 71

def test_find_cheapest_target():
    data = fetch_data('sample_data/day07.txt')
    assert find_cheapest_target(data) == (2, 37)

def test_align_on_pt2():
    data = fetch_data('sample_data/day07.txt')
    assert align_on_pt2(data, 5) == 168
    assert align_on_pt2(data, 2) == 206

def test_find_cheapest_target_pt2():
    data = fetch_data('sample_data/day07.txt')
    assert find_cheapest_target_pt2(data) == (5, 168)

#-----------------------------------------------------#

if __name__ == "__main__":
    data = fetch_data('data/day07.txt')
    print(find_cheapest_target_pt2(data))




