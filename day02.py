
def test_fetch_data_gives_tuples():
    data = list(fetch_data('sample_data/day02.txt'))
    assert data[0] == ('forward', 5)
    assert len(data) == 6

def test_calculate_position_pt1():
    data = fetch_data('sample_data/day02.txt')
    horizontal_pos, depth = calculate_position_pt1(data)
    assert horizontal_pos == 15
    assert depth == 10

def test_calculate_position_pt1():
    data = fetch_data('sample_data/day02.txt')
    horizontal_pos, depth = calculate_position_pt2(data)
    assert horizontal_pos == 15
    assert depth == 60



def fetch_data(path):
    with open(path, 'r') as f:
        for ln in f:
            dir, dist = ln.split()
            yield dir, int(dist)


def calculate_position_pt1(data):
    horizontal_pos, depth = 0, 0
    for dir, dist in data:
        if dir == 'forward': horizontal_pos += dist
        elif dir == 'down': depth += dist
        elif dir == 'up': depth -= dist
        else: raise ValueError('Unexpected instruction: ' + dir)
    return horizontal_pos, depth

def calculate_position_pt2(data):
    horizontal_pos, depth, aim = 0, 0, 0
    for dir, dist in data:
        if dir == 'forward': 
            horizontal_pos += dist
            depth += (aim * dist)
        elif dir == 'down': 
            aim += dist
        elif dir == 'up': 
            aim -= dist
        else: raise ValueError('Unexpected instruction: ' + dir)
    return horizontal_pos, depth

if __name__ == "__main__":
    data = fetch_data('data/day02.txt')
    horizontal_pos, depth = calculate_position_pt2(data)
    print(horizontal_pos * depth)
