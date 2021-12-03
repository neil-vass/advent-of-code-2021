
import statistics 

#------------------- tests ---------------------------#

def test_fetch_data():
    data = fetch_data('sample_data/day03.txt')
    assert data[0] == '00100'

def test_find_gamma_str_single_digits():
    data = ['1', '0', '1']
    assert find_gamma_str(data) == '1'

def test_find_gamma_str_double_digits():
    data = ['11', '00', '10']
    assert find_gamma_str(data) == '10'

def test_find_gamma_str_for_sample_data():
    data = fetch_data('sample_data/day03.txt')
    assert find_gamma_str(data) == '10110'

def test_find_epsilon_str():
    gamma = '10110'
    assert find_epsilon_str(gamma) == '01001'

def test_find_gamma_epsilon_values_for_sample_data():
    data = fetch_data('sample_data/day03.txt')
    gamma, epsilon = find_gamma_epsilon_values(data)
    assert gamma, epsilon == (22, 9)


#------------------- tests part 2---------------------#

def test_split_by_bit():
    data = ['11', '00', '10']
    assert split_by_bit(data, 0) == {'0': ['00'], '1': ['11', '10']}
    assert split_by_bit(data, 1) == {'0': ['00', '10'], '1': ['11']}

def test_find_o2_str():
    data = ['11', '00', '10']
    assert find_o2_str(data) == '11'

def test_find_o2_str_for_sample_data():
    data = fetch_data('sample_data/day03.txt')
    assert find_o2_str(data) == '10111'

def test_find_co2_str_for_sample_data():
    data = fetch_data('sample_data/day03.txt')
    assert find_co2_str(data) == '01010'

def test_find_o2_co2_values_for_sample_data():
    data = fetch_data('sample_data/day03.txt')
    o2, co2 = find_o2_co2_values(data)
    assert o2, co2 == (23, 10)

#-----------------------------------------------------#


def fetch_data(path):
    with open(path, 'r') as f:
        li = [ln.strip() for ln in f]
    return li

def find_gamma_str(data):
    gamma_str = ''
    for i in range(len(data[0])):
        column = (n[i] for n in data)
        gamma_str += statistics.mode(column)
    return gamma_str

def find_epsilon_str(gamma_str):
    inverter = str.maketrans('01', '10')
    return gamma_str.translate(inverter)

def find_gamma_epsilon_values(data):
    gamma_str = find_gamma_str(data)
    epsilon_str = find_epsilon_str(gamma_str)
    return int(gamma_str, base=2), int(epsilon_str, base=2)


def split_by_bit(data, bit_position):
    results = {'0': [], '1': []}
    for entry in data:
        results[entry[bit_position]].append(entry)
    return results


def find_o2_str(data):
     bit_position = 0
     values = data
     while True:
        candidate_lists = split_by_bit(values, bit_position)
        bit_position +=1

        if len(candidate_lists['1']) >= len(candidate_lists['0']):
            values = candidate_lists['1']
        else:
            values = candidate_lists['0']
        
        if len(values) == 1:
            return values[0]
            
            
def find_co2_str(data):
    bit_position = 0
    values = data
    while True:
        candidate_lists = split_by_bit(values, bit_position)
        bit_position +=1

        if len(candidate_lists['0']) <= len(candidate_lists['1']):
            values = candidate_lists['0']
        else:
            values = candidate_lists['1']
        
        if len(values) == 1:
            return values[0]

def find_o2_co2_values(data):
    o2_str = find_o2_str(data)
    co2_str = find_co2_str(data)
    return int(o2_str, base=2), int(co2_str, base=2) 


if __name__ == "__main__":
    data = fetch_data('data/day03.txt')
    o2, co2 = find_o2_co2_values(data)
    print(o2 * co2)
