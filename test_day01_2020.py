
import itertools, functools

def test_fetch_data_gives_ints():
    data = fetch_data()
    assert data[0] == 1801
    assert data[-1] == 1662
    
def test_find_combo_that_sums_to():
    li = [1,2,3]
    target = 4
    assert find_combo_that_sums_to(li, 2, target) == (1,3)

def fetch_data():
    with open('input_day01_2020.txt', 'r') as f:
        li = [int(x) for x in f]
    return li


def find_combo_that_sums_to(li, no_of_elements, target):
    return next(combo for combo in itertools.combinations(li, no_of_elements) if sum(combo) == target)





if __name__ == "__main__":
    elems = find_combo_that_sums_to(fetch_data(), 3, 2020)
    answer = functools.reduce(lambda x, y: x*y, elems)
    print(answer)
