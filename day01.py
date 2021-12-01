
# Thought SciPy would be useful; followed steps here to install it:
# https://solarianprogrammer.com/2016/10/04/install-python-numpy-scipy-matplotlib-macos/
# There's lots of advice about best ways to set it up, but pip just works.

def test_fetch_data_gives_ints():
    data = fetch_data('sample_data/day01.txt')
    assert data[0] == 199
    assert data[-1] == 263

def test_num_increases():
    assert num_increases([199, 200]) == 1
    assert num_increases([210, 200, 207, 240]) == 2

def test_sample_data_gives_correct_result():
    data = fetch_data('sample_data/day01.txt')
    assert num_increases(data) == 7


def fetch_data(path):
    with open(path, 'r') as f:
        li = [int(x) for x in f]
    return li

def num_increases(data):
    increases = 0 
    try:
        for idx, x in enumerate(data):
            if data[idx+1] > x:
                increases += 1
    except IndexError:
        pass
    return increases


if __name__ == "__main__":
    data = fetch_data('data/day01.txt')
    print(num_increases(data))
