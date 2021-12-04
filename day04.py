
import numpy as np
import numpy.ma as ma

class Board:
    def __init__(self, values):
        self._values = ma.masked_array(values, dtype=np.int64)
        
    def sum_of_unmarked_values(self):
        return np.sum(self._values)
    
    def is_winner(self): 
        marked = ma.getmaskarray(self._values)
        num_rows, num_cols = self._values.shape
        at_least_one_row_complete = any(all(marked[row,:]) for row in range(num_rows))
        at_least_one_col_complete = any(all(marked[:,col]) for col in range(num_cols))
        return at_least_one_row_complete or at_least_one_col_complete 

    def mark(self, n):
        hit = np.where(self._values == n)
        if len(hit[0]):
            self._values[hit] = ma.masked

    


def fetch_data(path):
    with open(path, 'r') as f:
        for ln in f:
            yield ln


#--------------------- tests -------------------------#

def test_board_setup():
    board = Board([[0, 1], 
                   [2, 3]])
    assert board._values[0,0] == 0
    assert board._values[1,0] == 2
    assert board.sum_of_unmarked_values() == 6
    assert not board.is_winner()

def test_board_mark_with_match():
    board = Board([[0, 1], 
                   [2, 3]])
    board.mark(1)
    assert board.sum_of_unmarked_values() == 5
    assert not board.is_winner()

def test_board_wins_when_whole_row_marked():
    board = Board([[0, 1], 
                   [2, 3]])
    board.mark(1)
    board.mark(0)
    assert board.sum_of_unmarked_values() == 5
    assert board.is_winner()

def test_board_wins_when_whole_col_marked():
    board = Board([[0, 1], 
                   [2, 3]])
    board.mark(1)
    board.mark(3)
    assert board.sum_of_unmarked_values() == 2
    assert board.is_winner()





#-----------------------------------------------------#

if __name__ == "__main__":
    print('Hello, World!')
