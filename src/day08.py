
def fetch_data(path):
    with open(path, 'r') as f:
        for ln in f:
            unique_patterns, display = [part.split() for part in ln.split('|')]
            yield unique_patterns, display


def identify_patterns(patterns):
    translator = {2: 1, 4: 4, 3: 7, 7: 8}
    return [(p, translator.get(len(p))) for p in patterns]

def count_easy_digits(data):
    count = 0
    for unique_patterns, display in data:
        count += len([d for d in identify_patterns(display) if d[1]])
    return count


#--------------------- tests -------------------------#

def test_fetch_data():
    data = fetch_data('sample_data/day08.txt')
    unique_patterns, display = next(data)
    assert len(unique_patterns) == 10
    assert unique_patterns[0] == 'be'
    assert len(display) == 4

def test_identify_patterns():
    data = fetch_data('sample_data/day08.txt')
    unique_patterns, display = next(data)
    assert identify_patterns(display) == [
        ('fdgacbe', 8), 
        ('cefdb', None), 
        ('cefbgd', None), 
        ('gcbe', 4)
    ]

def test_count_easy_digits():
    data = fetch_data('sample_data/day08.txt')
    assert count_easy_digits(data) == 26

#-----------------------------------------------------#

if __name__ == "__main__":
    data = fetch_data('data/day08.txt')
    print(count_easy_digits(data))
