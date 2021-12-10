

def first_invalid_char(ln):
    pairs = {'(': ')', '[': ']', '{': '}', '<': '>'}
    expected_matches = ''
    for c in ln:
        if c in pairs.keys():
            expected_matches += c
        else:
            if expected_matches == '':
                return c
            if c == pairs[expected_matches[-1]]:
                expected_matches = expected_matches[:-1]
            else:
                return c
    # For now, only report unexpected closings as problems.
    # There might be 'expected matches' we're still waiting for.
    return ''

def score_invalid_chars(data):
    scores = {')': 3, ']': 57, '}': 1197, '>': 25137}
    return sum([scores.get(first_invalid_char(ln), 0) for ln in data])


def fetch_data(path):
    with open(path, 'r') as f:
        for ln in f:
            yield ln.rstrip()

#--------------------- tests -------------------------#

def test_first_invald_char_gives_empty_when_valid():
    assert first_invalid_char('()') == ''
    assert first_invalid_char('[]') == ''
    assert first_invalid_char('{()()()}') == ''

def test_first_invald_char_gives_closer():
    assert first_invalid_char('(]') == ']'
    assert first_invalid_char('<([]){()}[{}])') == ')'

def test_score_invalid_chars():
    data = fetch_data('sample_data/day10.txt')
    assert score_invalid_chars(data) == 26397

#-----------------------------------------------------#

if __name__ == "__main__":
    data = fetch_data('data/day10.txt')
    print(score_invalid_chars(data))
