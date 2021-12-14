from collections import Counter

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

def _test_analyse_after_40_steps():
    template, rules = fetch_data('sample_data/day14.txt')
    assert analyse_after_step(template, rules, 40) == 2188189693529

#-----------------------------------------------------#

if __name__ == "__main__":
    template, rules = fetch_data('data/day14.txt')
    print(analyse_after_step(template, rules, 10))

    
