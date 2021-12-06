
def fetch_data(path):
    with open(path, 'r') as f:
        return [int(n) for n in f.readline().split(',')]

def simulate(initial_state, days):
    state = initial_state[:]
    for _ in range(days):
        babies = 0
        for idx in range(len(state)):
            if state[idx] == 0:
                state[idx] = 6
                babies += 1
            else:
                state[idx] -= 1
        state = state + [8] * babies
    return state

def simulate_v2(initial_state, days):
    school = dict.fromkeys(range(9), 0)
    for fish in initial_state:
        school[fish] += 1
    
    for _ in range(days):
        new_school = {}
        for i in range(8):
            new_school[i] = school[i+1]
        new_school[8] = school[0]
        new_school[6] += school[0]
        school = new_school

    return sum(school.values())

#--------------------- tests -------------------------#

def test_fetch_data():
    data = fetch_data('sample_data/day06.txt') 
    assert data == [3,4,3,1,2]

def test_simulate_single_fish():
    initial_state = [1]
    assert simulate(initial_state, 0) == [1]
    assert simulate(initial_state, 1) == [0]
    assert simulate(initial_state, 2) == [6,8]

def test_simulate():
    initial_state = fetch_data('sample_data/day06.txt')
    assert simulate(initial_state, 0) == initial_state
    assert simulate(initial_state, 1) == [2,3,2,0,1]
    assert simulate(initial_state, 2) == [1,2,1,6,0,8]
    assert simulate(initial_state, 3) == [0,1,0,5,6,7,8]

    assert len(simulate(initial_state, 18)) == 26
    assert len(simulate(initial_state, 80)) == 5934


def test_simulate_v2_single_fish():
    assert simulate_v2([0], 1) == 2
    assert simulate_v2([0], 29) == 17

def test_simulate_v2():
    initial_state = fetch_data('sample_data/day06.txt')
    assert simulate_v2(initial_state, 3) == 7
    assert simulate_v2(initial_state, 4) == 9
    assert simulate_v2(initial_state, 5) == 10
    assert simulate_v2(initial_state, 6) == 10
    assert simulate_v2(initial_state, 7) == 10
    assert simulate_v2(initial_state, 8) == 10
    assert simulate_v2(initial_state, 9) == 11
    assert simulate_v2(initial_state, 256) == 26984457539



#-----------------------------------------------------#

if __name__ == "__main__":
    initial_state = fetch_data('data/day06.txt')
    print(simulate_v2(initial_state, 256))
