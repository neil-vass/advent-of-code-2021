# Could probably just keep a dictionary of what cooridnates aren't zero - would mean we don't need to 
# specify a field size at the start. But, I like practicing numpy so I've used an array.
import numpy as np
import re

class Field:
    def __init__(self, x_width, y_width):
        self.matrix = np.zeros((x_width, y_width), dtype=np.int64)

    def mark(self, x1, y1, x2, y2):
        if x1 == x2:
            min_y = min(y1, y2)
            max_y = max(y1, y2) +1
            self.matrix[x1,...][min_y:max_y] += 1
        elif y1 == y2:
            min_x = min(x1, x2)
            max_x = max(x1, x2) +1
            self.matrix[min_x:max_x][...,y1] += 1
        else:
            # 45 degree diagonal
            cur_x, cur_y = x1, y1
            x_step = 1 if x2 > x1 else -1 
            y_step = 1 if y2 > y1 else -1
            self.matrix[cur_x, cur_y] += 1
            while cur_x != x2:
                cur_x += x_step
                cur_y += y_step
                self.matrix[cur_x, cur_y] += 1

    def mark_all(self, data):
        for entry in data:
            self.mark(*entry)

    def count_overlaps(self):
        return np.count_nonzero(self.matrix > 1)


def fetch_data(path):
    with open(path, 'r') as f:
        for ln in f:
            m = re.match(r'(\d+),(\d+) -> (\d+),(\d+)', ln)
            yield int(m[1]), int(m[2]), int(m[3]), int(m[4])

#--------------------- tests -------------------------#

def test_line_with_same_x_vals():
    field = Field(10, 10)
    field.mark(1,1, 1,3)
    assert field.matrix[1,1] == 1
    assert field.matrix[1,2] == 1
    assert field.matrix[1,3] == 1
    assert field.matrix.sum() == 3

def test_line_with_same_y_vals():
    field = Field(10, 10)
    field.mark(9,7, 7,7)
    assert field.matrix[9,7] == 1
    assert field.matrix[8,7] == 1
    assert field.matrix[7,7] == 1
    assert field.matrix.sum() == 3

def test_diagonal_line_is_marked():
    field = Field(10, 10)
    field.mark(1,1, 3,3)
    assert field.matrix[1,1] == 1
    assert field.matrix[2,2] == 1
    assert field.matrix[3,3] == 1
    assert field.matrix.sum() == 3

def test_overlaps():
    field = Field(10, 10)
    field.mark(0,9, 5,9)
    field.mark(0,9, 2,9)
    assert field.count_overlaps() == 3

def test_fetch_data():
    data = fetch_data('sample_data/day05.txt')
    assert next(data) == (0,9, 5,9)
    assert next(data) == (8,0, 0,8)

def test_sample_data_gives_correct_result():
    field = Field(10, 10)
    data = fetch_data('sample_data/day05.txt')
    field.mark_all(data)
    assert field.count_overlaps() == 12


#-----------------------------------------------------#

if __name__ == "__main__":
    field = Field(1000, 1000)
    data = fetch_data('data/day05.txt')
    field.mark_all(data)
    print(field.count_overlaps())
