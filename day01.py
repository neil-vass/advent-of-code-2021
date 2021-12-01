
def test_fetch_data_gives_ints():
    data = fetch_data('sample_data/day01.txt')
    assert data[0] == 199
    assert data[-1] == 263

def test_num_increases():
    assert num_increases([199, 200]) == 1
    assert num_increases([210, 200, 207, 240]) == 2

def test_sample_data_gives_correct_result_pt1():
    data = fetch_data('sample_data/day01.txt')
    assert num_increases(data) == 7

def test_sliding_window():
    data = fetch_data('sample_data/day01.txt')
    assert get_sliding_windows(data) == [607, 618, 618, 617, 647, 716, 769, 792]

def test_sample_data_gives_correct_result_pt2():
    data = fetch_data('sample_data/day01.txt')
    windows = get_sliding_windows(data)
    assert num_increases(windows) == 5




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

def get_sliding_windows(data):
    windows = []
    try:
        for idx, x in enumerate(data):
            window_sum = x + data[idx+1] + data[idx+2]
            windows.append(window_sum)
    except IndexError:
        pass
    return windows


if __name__ == "__main__":
    data = get_sliding_windows(fetch_data('data/day01.txt'))
    print(num_increases(data))
