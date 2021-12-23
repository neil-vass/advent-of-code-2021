# Unfinished! I'll come back to this one...

import re 

X,Y,Z = 0,1,2

class Report:

    def __init__(self, id, points):
        self.id = id
        self.points = points

    def translate(self, t):
        return Report(self.id, {(p[0]-t[0], p[1]-t[1], p[2]-t[2]) for p in self.points})

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
                    yield Report(self.id, {rot(p) for p in self.points}), rot


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


def find_overlaps(a, b, threshold=12):

    for translate_a_by in a.points:
        # Move a so one of its points is at the origin
        t0 = a.translate(translate_a_by)

        # Move b so one of its points is at the origin, move through all
        # rotations, then repeat for each point - and note which of these 
        # gives the most overlaps with a.
        for translate_b_by in b.points:
            t1 = b.translate(translate_b_by)

            for r1, rotation_function in t1.all_rotations():
                overlaps = t0.points & r1.points
                if len(overlaps) >= threshold: 
                    path_to_b = rotation_function(translate_b_by)
                    relative_scanner_position = tuple([translate_a_by[i] - path_to_b[i] for i in (X,Y,Z)])
                    overlaps = {tuple([ov[i] + translate_a_by[i] for i in (X,Y,Z)]) for ov in overlaps}
                    return overlaps, relative_scanner_position
    
    return None, None


def map_all_beacons(data, threshold=12):
    scanners_with_known_positions = {0: [(0,0,0), data[0]]}
    beacons = set()
    while len(scanners_with_known_positions) < len(data):
        known = list(scanners_with_known_positions.keys())
        for report in data:
            if report.id not in known:
                for k in known:
                    known_scanner_pos, known_report = scanners_with_known_positions[k]
                    overlaps, relative_scanner_position = find_overlaps(known_report, report, threshold)
                    if overlaps:
                        scanners_with_known_positions[report.id] = [
                            tuple([relative_scanner_position[i] - known_scanner_pos[i] for i in (X,Y,Z)]),
                            report
                        ]
                        overlaps = {tuple([ov[i] - known_scanner_pos[i] for i in (X,Y,Z)]) for ov in overlaps}
                        beacons |= overlaps
                        break
    return beacons, scanners_with_known_positions
                        

#--------------------- tests -------------------------#

def test_find_overlaps_same_scanner_different_orientations():
    data = fetch_data('sample_data/day19-same-scanner.txt')
    first = data[0]
    for other in data:
        overlaps, relative_scanner_position = find_overlaps(first, other, threshold=6)
        assert len(overlaps) == len(first.points)
        assert relative_scanner_position == (0,0,0)

def test_find_overlaps_different_scanners():
    data = fetch_data('sample_data/day19-different-scanners.txt')
    overlaps, relative_scanner_position = find_overlaps(data[0], data[1])
    assert len(overlaps) == 12
    assert (-618,-824,-621) in overlaps
    assert (-537,-823,-458) in overlaps
    assert relative_scanner_position == (68,-1246,-43)

def test_find_overlaps_scanners_1_and_4():
    data = fetch_data('sample_data/day19-different-scanners.txt')
    overlaps, relative_scanner_position = find_overlaps(data[1], data[4])
    assert len(overlaps) == 12


def test_map_all_beacons_for_same_scanner():
    data = fetch_data('sample_data/day19-same-scanner.txt')
    beacons, scanners_with_known_positions = map_all_beacons(data, threshold=6)
    assert len(beacons) == 6
    assert len(scanners_with_known_positions) == 5
    assert scanners_with_known_positions[0][1].points == scanners_with_known_positions[1][1].points

def test_map_all_beacons_for_0_1():
    data = fetch_data('sample_data/day19-different-scanners.txt')
    beacons, scanners_with_known_positions = map_all_beacons([data[0], data[1]])
    assert len(beacons) == 12
    assert set(scanners_with_known_positions.keys()) == {0,1}
    assert scanners_with_known_positions[1][0] == (68,-1246,-43)

def _test_map_all_beacons_for_0_1_4():
    data = fetch_data('sample_data/day19-different-scanners.txt')
    beacons, scanners_with_known_positions = map_all_beacons([data[0], data[1], data[4]])
    assert len(beacons) == 24
    assert set(scanners_with_known_positions.keys()) == {0,1,4}
    assert scanners_with_known_positions[4][0] == (-20,-1133,1061)

def _test_map_all_beacons():
    # I _think_ that once we find how scanners 0 and 1 overlap,
    # we then look for any beacons that overlap between 0 and 2, or 0 and 1.
    # Be careful not to double count any. And carry on through the growing list.
    data = fetch_data('sample_data/day19-different-scanners.txt')
    beacons, scanners_with_known_positions = map_all_beacons(data)
    assert scanners_with_known_positions[0][0] == (0,0,0)
    assert scanners_with_known_positions[1][0] == (68,-1246,-43)
    assert scanners_with_known_positions[2][0] == (1105,-1205,1229)
    assert scanners_with_known_positions[3][0] == (-92,-2380,-20)
    assert scanners_with_known_positions[4][0] == (-20,-1133,1061)
    assert len(beacons) == 79

#-----------------------------------------------------#

if __name__ == "__main__":
    print('Hello, World!')

