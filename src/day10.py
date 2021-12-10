
pairs = {'(': ')', '[': ']', '{': '}', '<': '>'}

def assess_line(ln):
    expected_matches = ''
    for c in ln:
        if c in pairs.keys():
            expected_matches += c
        else:
            if expected_matches == '':
                return c, expected_matches
            if c == pairs[expected_matches[-1]]:
                expected_matches = expected_matches[:-1]
            else:
                return c, expected_matches
    # For now, only report unexpected closings as problems.
    # There might be 'expected matches' we're still waiting for.
    return '', expected_matches

def first_invalid_char(ln):
    invalid, _ = assess_line(ln)
    return invalid

def score_invalid_chars(data):
    scores_map = {')': 3, ']': 57, '}': 1197, '>': 25137}
    return sum([scores_map.get(first_invalid_char(ln), 0) for ln in data])


def autocomplete(data):
    results = []
    for ln in data:
        invalid, expected_matches = assess_line(ln)
        if invalid == '':
            completion = ''.join(pairs[c] for c in expected_matches[::-1])
            results.append(completion)
    return results

def score_autocompletions(data):
    scores_map = {')': 1, ']': 2, '}': 3, '>': 4}
    scores = []
    for completion in autocomplete(data):
        total = 0
        for char in completion:
            total *= 5
            total += scores_map[char]
        scores.append(total)

    scores.sort()
    return scores[len(scores) // 2]


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

def test_autocomplete():
    assert autocomplete(['[({(<(())[]>[[{[]{<()<>>']) == ['}}]])})]']

def test_score_autocompletions():
    data = fetch_data('sample_data/day10.txt')
    assert score_autocompletions(data) == 288957

#-----------------------------------------------------#

if __name__ == "__main__":
    data = fetch_data('data/day10.txt')
    print(score_autocompletions(data))
