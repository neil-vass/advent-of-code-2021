import re 

X,Y,Z = 0,1,2

class Report:

    _rotations = [
        lambda x,y,z: ( x,  y,  z),
        lambda x,y,z: ( x,  z, -y),
        lambda x,y,z: ( x, -y, -z),
        lambda x,y,z: ( x, -z,  y),
        lambda x,y,z: (-x, -y,  z),
        lambda x,y,z: (-x,  z,  y),
        lambda x,y,z: (-x,  y, -z),
        lambda x,y,z: (-x, -z, -y),

        lambda x,y,z: ( y, -x,  z),
        lambda x,y,z: ( y,  z,  x),
        lambda x,y,z: ( y,  x, -z),
        lambda x,y,z: ( y, -z, -x),
        lambda x,y,z: (-y,  x,  z),
        lambda x,y,z: (-y,  z, -x),
        lambda x,y,z: (-y, -x, -z),
        lambda x,y,z: (-y, -z,  x),

        lambda x,y,z: ( z,  y, -x),
        lambda x,y,z: ( z, -x, -y),
        lambda x,y,z: ( z, -y,  x),
        lambda x,y,z: ( z,  x,  y),
        lambda x,y,z: (-z, -y, -x),
        lambda x,y,z: (-z, -x,  y),
        lambda x,y,z: (-z,  y,  x),
        lambda x,y,z: (-z,  x, -y)
    ]

    

    def __init__(self, id, points):
        self.id = id
        self.points = points

    def translate(self, t):
        return Report(self.id, {(p[0]-t[0], p[1]-t[1], p[2]-t[2]) for p in self.points})


    def _all_rotations(self):
        for rot in Report._rotations:
            yield Report(self.id, {rot(*p) for p in self.points})


    def rot_fun(facing, first_rot, second_rot, flip_axis, rotation_steps):
        ordering = [facing, first_rot, second_rot]
        signs = [1, 1, 1]

        if flip_axis:
            ordering = [facing, second_rot, first_rot]
            signs = [-1, 1, 1]

        for _ in range(rotation_steps):
            ordering[1], ordering[2] = ordering[2], ordering[1]
            signs[1], signs[2] = (signs[2] * -1), signs[1]

        return lambda p: tuple([p[ordering[i]]*signs[i] for i in range(3)])


    def all_rotations(self):
        for facing, first_rot, second_rot in [(X,Y,Z),(Y,Z,X),(Z,X,Y)]:
            for flip_axis in (False, True):
                for rotation_steps in range(4):
                    rot = Report.rot_fun(facing, first_rot, second_rot, flip_axis, rotation_steps)
                    yield Report(self.id, {rot(p) for p in self.points})

    # Rotate by 90 degrees around a fixed axis.
    def _rotate(self, first_rot, second_rot):
        new_points = set()
        for p in self.points:
            rotated_p = list(p)
            rotated_p[first_rot] = -p[second_rot]
            rotated_p[second_rot] = p[first_rot]               
            new_points.add(tuple(rotated_p))
        return Report(id, new_points)

    def _set_facing(self, facing_axis):
        new_points = set()
        for p in self.points:
            facing_p = list(p)
            facing_p[0] = p[facing_axis]
            facing_p[facing_axis] = -p[0]
            new_points.add(tuple(facing_p))
        return Report(id, new_points)

    def _flip_axis(self, flip_axis, mirrored_axis):
        new_points = set()
        for p in self.points:
            rotated_p = list(p)
            rotated_p[flip_axis] = -p[flip_axis]
            rotated_p[mirrored_axis] = -p[mirrored_axis]
            new_points.add(tuple(rotated_p))
        return Report(id, new_points)

def fetch_data(path):
    data = []
    with open(path, 'r') as f:
        for ln in f:
            m = re.match(r'--- scanner (\d+) ---', ln)
            if m:
                id = int(m[1])
                points = set()
            else:
                m = re.match(r'(-?\d+),(-?\d+),(-?\d+)', ln)
                if m:
                    points.add((int(m[1]), int(m[2]), int(m[3])))
                else:
                    data.append(Report(id, points))
        data.append(Report(id, points))
    return data


def find_overlaps(a, b):
    most_overlaps = 0

    # Move a so one of its points is at the origin
    t0 = a.translate(next(iter(a.points)))

    # Move b so one of its points is at the origin, move through all
    # rotations, then repeat for each point - and note which of these 
    # gives the most overlaps with a.
    for p in b.points:
        t1 = b.translate(p)

        for r1 in t1.all_rotations():
            overlaps = len(t0.points & r1.points)
            if overlaps > most_overlaps: 
                most_overlaps = overlaps

    return most_overlaps



#--------------------- tests -------------------------#

def test_find_overlaps_in_2d():
    z = 0
    a = Report(0, {(0,2,z), (4,1,z), (3,3,z)})
    b = Report(1, {(-1,-1,z), (-5,0,z), (-2,1,z)})
    assert find_overlaps(a, b) == 3


def test_find_overlaps_same_scanner_different_orientations():
    data = fetch_data('sample_data/day19-same-scanner.txt')
    first = data[0]
    for other in data:
        assert find_overlaps(first, other) == len(first.points)


#-----------------------------------------------------#

if __name__ == "__main__":
    print('Hello, World!')

