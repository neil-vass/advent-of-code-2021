
# Thought SciPy would be useful; followed steps here to install it:
# https://solarianprogrammer.com/2016/10/04/install-python-numpy-scipy-matplotlib-macos/
# There's lots of advice about best ways to set it up, but pip just works.

def test_fetch_data_gives_ints():
    data = fetch_data()
    assert data[0] == 199
    assert data[-1] == 263
    


def fetch_data():
    with open('small_inputs/day01.txt', 'r') as f:
        li = [int(x) for x in f]
    return li




if __name__ == "__main__":
    print('Hello, World!')
