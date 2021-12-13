import numpy as np
import re

class Paper:
    def __init__(self, dots):
        x, y = zip(*dots)
        self.grid = np.zeros((max(x)+1, max(y)+1), dtype=bool)
        self.grid[x,y] = 1

    def fold(self, fold):
        axis, index = fold
        if axis == 'x':
            keep = self.grid[:index,...]
            folded = self.grid[index+1:,...]
            folded = np.flip(folded, axis=0)
        else:
            keep = self.grid[...,:index]
            folded = self.grid[...,index+1:]
            folded = np.flip(folded, axis=1)
        keep |= folded
        self.grid = keep

    def visible_dots(self):
        return np.count_nonzero(self.grid)

    def display(self):
        display = []
        for row in self.grid.transpose():
            display.append(''.join('#' if d else '.' for d in row))
        return display


def fetch_data(path):
    with open(path, 'r') as f:
        dots, folds = [],[]
        for ln in f: 
            dot_match = re.match(r'(\d+),(\d+)', ln)
            if dot_match:
                dots.append((int(dot_match[1]), int(dot_match[2])))
            else:
                fold_match = re.match(r'fold along (.)=(\d+)', ln)
                if fold_match:
                    folds.append((fold_match[1], int(fold_match[2])))
    return dots, folds


#--------------------- tests -------------------------#

def test_fetch_data():
    dots, folds = fetch_data('sample_data/day13.txt')
    assert len(dots) == 18
    assert dots[:3] == [(6,10), (0,14), (9,10)]
    assert folds == [('y', 7), ('x', 5)]

def test_create_and_fold():
    dots, folds = fetch_data('sample_data/day13.txt')
    paper = Paper(dots)
    assert paper.visible_dots() == 18
    paper.fold(folds[0])
    assert paper.visible_dots() == 17
    paper.fold(folds[1])
    assert paper.visible_dots() == 16

def test_display():
    dots, folds = fetch_data('sample_data/day13.txt')
    paper = Paper(dots)
    for f in folds:
        paper.fold(f)
    display = paper.display()
    assert display[0] == '#####'
    assert display[1] == '#...#'

#-----------------------------------------------------#

if __name__ == "__main__":
    dots, folds = fetch_data('data/day13.txt')
    paper = Paper(dots)
    for f in folds:
        paper.fold(f)
    for row in paper.display():
        print(row)
