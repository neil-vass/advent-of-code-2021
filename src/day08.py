
from os import X_OK


def parse_line(ln):
    unique_patterns, display = [part.split() for part in ln.split('|')]
    return unique_patterns, display

def fetch_data(path):
    with open(path, 'r') as f:
        for ln in f:
            yield parse_line(ln)


def identify_easy_digits(patterns):
    translator = {2: 1, 4: 4, 3: 7, 7: 8}
    return [(p, translator.get(len(p))) for p in patterns]

def count_easy_digits(data):
    count = 0
    for unique_patterns, display in data:
        count += len([d for d in identify_easy_digits(display) if d[1]])
    return count

def identify_all_digits(unique_patterns):
    # Get the easy digits: 1, 4, 7, 8
    digits_to_strings = dict([(b,a) for a,b in identify_easy_digits(unique_patterns) if b])
    
    digits_to_strings[6] = [p for p in unique_patterns if len(p) == 6 and not set(p) >= set(digits_to_strings[1])][0]
    digits_to_strings[3] = [p for p in unique_patterns if len(p) == 5 and set(p) >= set(digits_to_strings[1])][0]
    
    top_right_line = list(set(digits_to_strings[8]) - set(digits_to_strings[6]))[0]

    digits_to_strings[5] = [p for p in unique_patterns if len(p) == 5 and top_right_line not in p][0]
    digits_to_strings[2] = [p for p in unique_patterns if len(p) == 5 and p not in (digits_to_strings[3], digits_to_strings[5])][0]

    bottom_left_line = list(set(digits_to_strings[6]) - set(digits_to_strings[5]))[0]
    
    digits_to_strings[9] = [p for p in unique_patterns if len(p) == 6 and bottom_left_line not in p][0]
    digits_to_strings[0] = [p for p in unique_patterns if len(p) == 6 and p not in (digits_to_strings[6], digits_to_strings[9])][0]

    strings_to_digits = {v: k for k, v in digits_to_strings.items()}
    return strings_to_digits

def read_output(unique_patterns, display):
    strings_to_digits = identify_all_digits(unique_patterns)
    
    units = 1
    result = 0
    for digit in display[::-1]:
        for key in strings_to_digits.keys():
            if set(key) == set(digit):
                result += (strings_to_digits[key] * units)
                break
        units *= 10
    return result

def combine_display_values(data):
    return sum(read_output(unique_patterns, display) for unique_patterns, display in data)


#--------------------- tests -------------------------#

def test_fetch_data():
    data = fetch_data('sample_data/day08.txt')
    unique_patterns, display = next(data)
    assert len(unique_patterns) == 10
    assert unique_patterns[0] == 'be'
    assert len(display) == 4

def test_identify_easy_digits():
    data = fetch_data('sample_data/day08.txt')
    unique_patterns, display = next(data)
    assert identify_easy_digits(display) == [
        ('fdgacbe', 8), 
        ('cefdb', None), 
        ('cefbgd', None), 
        ('gcbe', 4)
    ]

def test_count_easy_digits():
    data = fetch_data('sample_data/day08.txt')
    assert count_easy_digits(data) == 26

def test_identify_all_digits():
    ln = 'acedgfb cdfbe gcdfa fbcad dab cefabd cdfgeb eafb cagedb ab | cdfeb fcadb cdfeb cdbaf'
    unique_patterns, display = parse_line(ln)
    assert identify_all_digits(unique_patterns) == {
        'acedgfb': 8, 
        'cdfbe': 5, 
        'gcdfa': 2,
        'fbcad': 3,
        'dab': 7,
        'cefabd': 9,
        'cdfgeb': 6,
        'eafb': 4,
        'cagedb': 0,
        'ab': 1
    }

def test_read_output():
    ln = 'acedgfb cdfbe gcdfa fbcad dab cefabd cdfgeb eafb cagedb ab | cdfeb fcadb cdfeb cdbaf'
    unique_patterns, display = parse_line(ln)
    assert read_output(unique_patterns, display) == 5353

def test_combine_display_values():
    data = fetch_data('sample_data/day08.txt')
    assert combine_display_values(data) == 61229


#-----------------------------------------------------#

if __name__ == "__main__":
    data = fetch_data('data/day08.txt')
    print(combine_display_values(data))
