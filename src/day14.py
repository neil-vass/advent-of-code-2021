from collections import Counter, defaultdict

def fetch_data(path):
    with open(path, 'r') as f:
        template = f.readline().rstrip()
        f.readline()

        rules = {}
        for ln in f:
            pair, arrow, elem = ln.rstrip().split()
            rules[pair] = elem
        return template, rules

def apply_rules(polymer, rules):
    updated_polymer = polymer[0]
    for i in range(len(polymer)-1):
        left, right = polymer[i], polymer[i+1]
        updated_polymer += rules.get(left+right, '') + right
    return updated_polymer

def analyse_after_step(polymer, rules, steps):
    for _ in range(steps):
        polymer = apply_rules(polymer, rules)
    counts = Counter(polymer).most_common()
    return counts[0][1] - counts[-1][1]

#--------------- Part 2: use dicts of pairs rather than whole string -----------------#

# Gives a dict of (pair, number of times pair occurs)
def polymer_to_pairs(polymer):
    polymer_as_pairs = defaultdict(int)   
    for i in range(len(polymer)-1):
        pair = polymer[i:i+2]
        polymer_as_pairs[pair] += 1
    return polymer_as_pairs

# Pairs are overlapping, so to get count of elements:
# Count just the 2nd element in each pair, 
# and add on 1 count of the element at the start of the polymer.
def counts_of_elements(polymer_as_pairs, first_elem_in_polymer):
    counts = Counter()
    counts[first_elem_in_polymer] = 1
    for pair, val in polymer_as_pairs.items():
        counts[pair[1]] += val
    return counts

def apply_rules_pt2(polymer_as_pairs, rules):
    updated_polymer = defaultdict(int)
    for pair in polymer_as_pairs:
        if pair in rules:
            left = pair[0] + rules[pair]
            right =  rules[pair] + pair[1]
            updated_polymer[left] += polymer_as_pairs[pair]
            updated_polymer[right] += polymer_as_pairs[pair]
        else:
            updated_polymer[pair] += polymer_as_pairs[pair]
    return updated_polymer    


def analyse_after_step_pt2(polymer, rules, steps):
    polymer_as_pairs = polymer_to_pairs(polymer)
    for _ in range(steps):
        polymer_as_pairs = apply_rules_pt2(polymer_as_pairs, rules)
    counts = counts_of_elements(polymer_as_pairs, polymer[0]).most_common()
    return counts[0][1] - counts[-1][1]



#--------------------- tests -------------------------#

def test_fetch_data():
    template, rules = fetch_data('sample_data/day14.txt')
    assert template == 'NNCB'
    assert len(rules) == 16
    assert rules['CB'] == 'H'

def test_apply_rules():
    template, rules = fetch_data('sample_data/day14.txt')
    polymer = apply_rules(template, rules)
    assert polymer == 'NCNBCHB'

def test_apply_rules_multiple_times():
    polymer, rules = fetch_data('sample_data/day14.txt')
    for _ in range(10):
        polymer = apply_rules(polymer, rules)
    assert len(polymer) == 3073

def test_analyse_after_10_steps():
    template, rules = fetch_data('sample_data/day14.txt')
    assert analyse_after_step(template, rules, 10) == 1588

def test_polymer_to_pairs():
    assert polymer_to_pairs('NNCB') == {'NN': 1, 'NC': 1, 'CB': 1}

def test_apply_rules_pt2():
    template, rules = fetch_data('sample_data/day14.txt')
    polymer = polymer_to_pairs(template)
    polymer = apply_rules_pt2(polymer, rules)
    assert polymer == {'NC': 1, 'CN': 1, 'NB': 1, 'BC': 1, 'CH': 1, 'HB': 1}

def test_counts_of_elements():
    template, rules = fetch_data('sample_data/day14.txt')
    polymer = polymer_to_pairs(template)
    counts = counts_of_elements(polymer, first_elem_in_polymer='N')
    assert counts['N'] == 2
    assert counts['C'] == 1
    assert counts['B'] == 1

def test_analyse_pt2_after_10_steps():
    template, rules = fetch_data('sample_data/day14.txt')
    assert analyse_after_step_pt2(template, rules, 10) == 1588

def test_analyse_after_40_steps():
    template, rules = fetch_data('sample_data/day14.txt')
    assert analyse_after_step_pt2(template, rules, 40) == 2188189693529

#-----------------------------------------------------#

if __name__ == "__main__":
    template, rules = fetch_data('data/day14.txt')
    print(analyse_after_step_pt2(template, rules, 40))

    
