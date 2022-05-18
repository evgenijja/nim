import random

def generate_piles(n, m):
    "Generates random number of piles (between 1 and n) each with random number of coins (between 1 and m)"
    game = []
    num_piles = random.randint(1, n)
    for i in range(num_piles):
        num_coins = random.randint(1, m)
        game.append(num_coins)
    return game



class Nim():

    def __init__(self, initial):
        "Initialize game"
        "piles .... list of numbers - each number represents # of coins in each pile"
        "player ... 0 or 1"
        "winner ... 0 or 1 or -1 (-1 means no winner yet)"
        self.piles = initial.copy()
        self.player = 0
        self.winner = -1



    def possible_actions(self):
        "Returns all possible actions for a given set of piles"
        "action (i, j) means take j coins from i-th pile"        
        actions = []
        for i in range(len(self.piles)):
            for j in range(1, self.piles[i]): # player has to take at least one coin
                actions.append((i, j))
        return actions



    def switch_player(self):
        "Switches player"
        self.player = 0 if self.player == 1 else 1



    def check_for_winner(self):
        "Checks for winner - returns True if winner found, else it returns False"
        "First player makes a move, then we switch player, then we check for winner"
        "If there are no piles left that means other player took the last one and the player that is on the move won"

        counter = 0
        for pile in self.piles:
            if pile == 0:
                counter += 1
        if counter == len(self.piles):
            self.winner = self.player
            return True
        return False



    def make_move(self, action):
        "Makes move and switches player"

        if self.winner == -1:
            (i, j) = action # take j coins from i-th pile
            self.piles[i] -= j
            self.switch_player()
            self.check_for_winner()
        else:
            raise Exception("Winner already determined")


