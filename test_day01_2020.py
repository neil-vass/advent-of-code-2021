
import itertools

def test_fetch_data_gives_ints():
    data = fetch_data()
    assert data[0] == 1721
    assert data[-1] == 1456
    
def test_find_pair_that_sums_to():
    li = [1,2,3]
    target = 4
    assert find_pair_that_sums_to(li, target) == (1,3)

def fetch_data():
    with open('input_day01_2020.txt', 'r') as f:
        li = [int(x) for x in f]
    return li


def find_pair_that_sums_to(li, target):
    return next(pair for pair in itertools.combinations(li, 2) if sum(pair) == target)





if __name__ == "__main__":
    x, y = find_pair_that_sums_to(fetch_data(), 2020)
    print(x * y)

