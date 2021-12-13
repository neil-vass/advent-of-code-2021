from collections import defaultdict

class Caves:
    def __init__(self, lines):
        self.graph = defaultdict(list)
        for ln in lines:
            left, right = ln.split('-')
            self.graph[left].append(right)
            self.graph[right].append(left)

    def find_paths_from(self, so_far):  
        # Check if we've done 2 vists to any small cave yet
        small_caves = [c for c in so_far if c.islower()]
        dbl_visit_done = len(small_caves) > len(set(small_caves))

        if dbl_visit_done:
            next_steps = [n for n in self.graph[so_far[-1]] if n.isupper() or n not in so_far]
        else:
            next_steps = [n for n in self.graph[so_far[-1]] if n != 'start']
        
        if next_steps:
            options = []
            for n in next_steps:
                if n == 'end':
                    options += [so_far + [n]]
                else:
                    options += self.find_paths_from(so_far + [n])
            return options
        else:
            return [so_far]

    def find_paths(self):
        paths_as_lists = self.find_paths_from(['start'])
        return set([','.join(p) for p in paths_as_lists if p[-1] == 'end'])

def fetch_data(path):
    with open(path, 'r') as f:
        for ln in f:
            yield ln.rstrip()

#--------------------- tests -------------------------#

def test_find_paths_base_case():
    lines = ['start-end']
    caves = Caves(lines)
    assert caves.find_paths() == {'start,end'}

def test_find_paths_with_branch():
    lines = [
        'start-a',
        'start-b',
        'a-end',
        'b-end'
    ]
    caves = Caves(lines)
    assert caves.find_paths() == {'start,a,end', 'start,b,end'}

def test_find_paths_in_sample1():
    data = fetch_data('sample_data/day12-sample1.txt')
    caves = Caves(data)
    assert len(caves.find_paths()) == 36

def test_find_paths_in_sample2():
    data = fetch_data('sample_data/day12-sample2.txt')
    caves = Caves(data)
    assert len(caves.find_paths()) == 103

def test_find_paths_in_sample3():
    data = fetch_data('sample_data/day12-sample3.txt')
    caves = Caves(data)
    assert len(caves.find_paths()) == 3509

#-----------------------------------------------------#

if __name__ == "__main__":
    data = fetch_data('data/day12.txt')
    caves = Caves(data)
    print(len(caves.find_paths()))
