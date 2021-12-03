
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

def test_find_values_for_sample_data():
    data = fetch_data('sample_data/day03.txt')
    gamma, epsilon = find_values(data)
    assert gamma, epsilon == (22, 9)

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

def find_values(data):
    gamma_str = find_gamma_str(data)
    epsilon_str = find_epsilon_str(gamma_str)
    return int(gamma_str, base=2), int(epsilon_str, base=2)


if __name__ == "__main__":
    data = fetch_data('data/day03.txt')
    gamma, epsilon = find_values(data)
    print(gamma * epsilon)
