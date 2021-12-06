
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
        draws = [int(n) for n in f.readline().split(',')]
        boards = []
        f.readline()
        values = []
        for ln in f:
            if len(ln) <= 1:
                boards.append(Board(values))
                values = []
            else:
                values.append([int(n) for n in ln.split()])
        
        return draws, boards


def find_winner(draws, boards):
    for draw in draws:
        for board in boards:
            board.mark(draw)
            if board.is_winner():
                return draw, board

def find_loser(draws, boards):
    boards_left = len(boards)
    for draw in draws:
        for board in boards:
            if not board.is_winner():
                board.mark(draw)
                if board.is_winner():
                    boards_left -=1
                if boards_left == 0:
                    return draw, board
                

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



def test_fetch_data():
    draws, boards = fetch_data('sample_data/day04.txt')
    assert draws[:3] == [7,4,9]
    assert len(boards) == 3
    assert boards[1]._values[0, 0] == 3

def test_find_winner_with_sample_data():
    draws, boards = fetch_data('sample_data/day04.txt')
    last_draw, board = find_winner(draws, boards)
    assert last_draw == 24
    assert board.sum_of_unmarked_values() == 188

def test_find_loser_with_sample_data():
    draws, boards = fetch_data('sample_data/day04.txt')
    last_draw, board = find_loser(draws, boards)
    assert last_draw == 13
    assert board.sum_of_unmarked_values() == 148

#-----------------------------------------------------#

if __name__ == "__main__":
    draws, boards = fetch_data('data/day04.txt')
    last_draw, board = find_loser(draws, boards)
    print(last_draw * board.sum_of_unmarked_values())
