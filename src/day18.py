
import math
import ast
import itertools
import copy

class SN:
    def __init__(self, value):
        assert len(value) == 2, 'SN value must be a pair'
        self.value = value
    
    @staticmethod
    def _find_path_to_first_pair_nested_in_4(current_pair, path_so_far=None):
        if path_so_far is None:
            path_so_far = []
        
        for i in (0,1):
            if type(current_pair[i]) is list:
                if len(path_so_far) == 3:
                    return path_so_far + [i]
                else: 
                    path_through_this_elem = SN._find_path_to_first_pair_nested_in_4(current_pair[i], path_so_far + [i])
                    if path_through_this_elem:
                        return path_through_this_elem
        return None

    def _follow_the_path(self, path):
        pair = self.value
        for idx in path:
            pair = pair[idx]
        return pair

    def _explode(self):
        path_to_explodable = SN._find_path_to_first_pair_nested_in_4(self.value)
        if not path_to_explodable:
            return False

        left, right = self._follow_the_path(path_to_explodable)
        
        # If there's any 1's in the path (we took the right), there'll be a number to add to there.
        # May need to drill into pairs till we find it.
        try:
            idx_to_left = max(idx for idx, val in enumerate(path_to_explodable) if val == 1)
            to_update = self._follow_the_path(path_to_explodable[:idx_to_left])
            if type(to_update[0]) is int:
                to_update[0] += left
            else:
                to_update = to_update[0]
                while type(to_update[1]) is list:
                    to_update = to_update[1]
                to_update[1] += left
        except ValueError:
            pass

        # Adding to the right is similar.
        try:
            idx_to_right = max(idx for idx, val in enumerate(path_to_explodable) if val == 0)
            to_update = self._follow_the_path(path_to_explodable[:idx_to_right])
            if type(to_update[1]) is int:
                to_update[1] += right
            else:
                to_update = to_update[1]
                while type(to_update[0]) is list:
                    to_update = to_update[0]
                to_update[0] += right
        except ValueError:
            pass
     
        # Then, replace our [] pair with the number zero.
        self._follow_the_path(path_to_explodable[:-1])[path_to_explodable[-1]] = 0
        return True

    @staticmethod
    def _find_path_to_first_double_digit_num(current_pair, path_so_far=None):
        if path_so_far is None:
            path_so_far = []
        
        for i in (0,1):
            if type(current_pair[i]) is list:
                path_through_this_elem = SN._find_path_to_first_double_digit_num(current_pair[i], path_so_far + [i])
                if path_through_this_elem:
                    return path_through_this_elem
            else: 
                if current_pair[i] > 9:
                    return path_so_far + [i]
        return None

    def _split(self):
        path_to_splittable = SN._find_path_to_first_double_digit_num(self.value)
        if not path_to_splittable:
            return False

        half_val = self._follow_the_path(path_to_splittable) / 2
        parent = self._follow_the_path(path_to_splittable[:-1])
        parent[path_to_splittable[-1]] = [math.floor(half_val), math.ceil(half_val)]
        return True


    def _reduce(self):
        while True:
            exploded = self._explode()
            if not exploded:
                splitted = self._split()
                if not splitted:
                    break

    def magnitude(self):
        left, right = self.value
        left_mag = left if type(left) is int else SN(left).magnitude()
        right_mag = right if type(right) is int else SN(right).magnitude()
        return left_mag * 3 + right_mag * 2


    def __add__(self, other):
        num = SN([copy.deepcopy(self.value), copy.deepcopy(other.value)])
        num._reduce()
        return num

    def __eq__(self, other):
        return self.value == other.value


def fetch_data(path):
    data = []
    with open(path, 'r') as f:
        for ln in f:
            li = ast.literal_eval(ln)
            data.append(SN(li))
    return data


def largest_mag_from_adding_two(data):
    return max((a+b).magnitude() for a,b in itertools.permutations(data, 2))

#--------------------- tests -------------------------#

def test_basics():
    assert SN([1,2]) == SN([1,2])
    assert SN([1,2]) != SN([2,1])
    assert SN([1,2]) + SN([[3,4],5]) == SN([[1,2],[[3,4],5]])

# Testing internals of the class
def test_find_path_to_first_pair_nested_in_4():
    num = SN([[[[[9,8],1],2],3],4])
    path = SN._find_path_to_first_pair_nested_in_4(num.value)
    assert path == [0,0,0,0]
    pair = num.value
    for idx in path:
        pair = pair[idx]
    assert pair == [9,8]

def test_explode_with_no_num_to_left():
    num = SN([[[[[9,8],1],2],3],4])
    num._explode()
    assert num == SN([[[[0,9],2],3],4])

def test_explode_with_no_num_to_right():
    num = SN([7,[6,[5,[4,[3,2]]]]])
    num._explode()
    assert num == SN([7,[6,[5,[7,0]]]])

def test_explode_with_nums_both_directions():
    num = SN([[6,[5,[4,[3,2]]]],1])
    num._explode()
    assert num == SN([[6,[5,[7,0]]],3])

def test_explode_takes_first_suitable_pair():
    num = SN([[3,[2,[1,[7,3]]]],[6,[5,[4,[3,2]]]]])
    print(SN._find_path_to_first_pair_nested_in_4(num.value))
    num._explode()
    assert num == SN([[3,[2,[8,0]]],[9,[5,[4,[3,2]]]]])

def test_explode_with_last_example():
    num = SN([[3,[2,[8,0]]],[9,[5,[4,[3,2]]]]])
    print(SN._find_path_to_first_pair_nested_in_4(num.value))
    num._explode()
    assert num == SN([[3,[2,[8,0]]],[9,[5,[7,0]]]])


def test_split():
    num = SN([[10,5],11])
    num._split()
    assert num == SN([[[5,5],5],11])

def test_addition_with_reduce():
    a = SN([[[[4,3],4],4],[7,[[8,4],9]]])
    b = SN([1,1])
    print((a+b).value)
    assert a + b == SN([[[[0,7],4],[[7,8],[6,0]]],[8,1]])

def test_multiple_additions():
    result = (
        SN([1,1]) + 
        SN([2,2]) + 
        SN([3,3]) + 
        SN([4,4]) + 
        SN([5,5]) + 
        SN([6,6])
    )
    assert result == SN([[[[5,0],[7,4]],[5,5]],[6,6]])

def test_fetch_data():
    data = fetch_data('sample_data/day18.txt')
    assert len(data) == 10
    assert data[0] == SN([[[0,[4,5]],[0,0]],[[[4,5],[2,6]],[9,5]]])

def test_additions_from_file():
    data = fetch_data('sample_data/day18.txt')
    num = data[0]
    for sn in data[1:]:
        num += sn
    assert num == SN([[[[8,7],[7,7]],[[8,6],[7,7]]],[[[0,7],[6,6]],[8,7]]])

def test_magnitude():
    assert SN([9,1]).magnitude() == 29
    assert SN([[1,2],[[3,4],5]]).magnitude() == 143
    assert SN([[[[8,7],[7,7]],[[8,6],[7,7]]],[[[0,7],[6,6]],[8,7]]]).magnitude() == 3488

def test_largest_mag_from_adding_two():
    data = fetch_data('sample_data/day18-pt2.txt')
    assert largest_mag_from_adding_two(data) == 3993

#-----------------------------------------------------#

if __name__ == "__main__":
    data = fetch_data('data/day18.txt')
    print(largest_mag_from_adding_two(data))