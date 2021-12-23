
POS, SCORE = 0,1

class Game:

    def __init__(self, starting_positions):
        self.state = [[pos, 0] for pos in starting_positions]
        self.next_die_val = 0
        self.die_rolls = 0

    def roll(self):
        self.die_rolls += 1
        self.next_die_val += 1
        if self.next_die_val > 100:
            self.next_die_val = 1
        return self.next_die_val

    def results(self):
        return min([player[SCORE] for player in self.state]) * self.die_rolls

    
    def play(self):
        while True:
            for player in self.state:
                pos_before_wrap = player[POS] + sum([self.roll(), self.roll(), self.roll()])
                player[POS] = ((pos_before_wrap -1) % 10) + 1
                player[SCORE] += player[POS]
                if player[SCORE] >= 1000:
                    return self.results()

    

                

#--------------------- tests -------------------------#

def test_game():
    game = Game([4, 8])
    assert game.play() == 739785

#-----------------------------------------------------#

if __name__ == "__main__":
    game = Game([4, 9])
    print(game.play())
