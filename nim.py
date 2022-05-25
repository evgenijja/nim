import copy
import random
from math import inf


def generate_piles(n, m):
    """Generates random number of piles (between 1 and n) each with random number of coins (between 1 and m)"""
    game = []
    num_piles = random.randint(1, n)
    for i in range(num_piles):
        num_coins = random.randint(1, m)
        game.append(num_coins)
    return game


def play_in_console():
    input1 = input("Vpisi seznam stevil, ki predstavljajo zacetno st. predmetov v kupcku. (npr: 4 5 6):  ")
    game = list(map(lambda x: int(x.strip()), input1.strip().split(" ")))
    print("Zacetno stanje: ", game, "Zacne igralec 0.")
    print(
        "na vsakem koraku vpisi potezo v obliki para stevil. npr: 3 4 pomeni, da iz tretjega kupcka odstranis 4 predmete.")
    nim = Nim(game)
    while not nim.check_for_winner():
        poteza = input(f"Igralec {nim.player}: vpisi potezo: ")
        x, y = list(map(lambda x: int(x.strip()), poteza.strip().split(" ")))
        nim.make_move((x - 1, y))
        print(nim.piles)
    print(f"Zmagal je igralec {nim.player}!")


def play_in_console_vs_minimax():
    input1 = input("Vpisi seznam stevil, ki predstavljajo zacetno st. predmetov v kupcku. (npr: 4 5 6):  ")
    game = list(map(lambda x: int(x.strip()), input1.strip().split(" ")))
    print("Zacetno stanje: ", game, "Zacne igralec 0.")
    print("Na vsakem koraku vpisi potezo v obliki para stevil. npr: 3 4 pomeni, da iz tretjega kupcka odstranis 4 predmete.")
    nim = Nim(game)
    while not nim.check_for_winner():
        if nim.player == 0:
            poteza = input(f"Igralec {nim.player}: vpisi potezo: ")
            x, y = list(map(lambda z: int(z.strip()), poteza.strip().split(" ")))
            nim.make_move((x - 1, y))
        else:
            # poteza algoritma
            nim.minimax_play(4)
        print(nim.piles)

    print(f"Zmagal je igralec {nim.player}!")


class Nim:

    def __init__(self, initial):
        """Initialize game
        piles .... list of numbers - each number represents # of coins in each pile
        player ... 0 or 1
        winner ... 0 or 1 or -1 (-1 means no winner yet)"""
        self.piles = initial.copy()
        self.player = 0
        self.winner = -1

    def possible_actions(self):
        """
        Returns all possible actions for a given set of piles
        action (i, j) means take j coins from i-th pile"""
        actions = []
        for i in range(len(self.piles)):
            for j in range(1, self.piles[i] + 1):  # player has to take at least one coin
                actions.append((i, j))
        return actions

    def switch_player(self):
        """Switches player"""
        self.player = 0 if self.player == 1 else 1

    def check_for_winner(self):
        """Checks for winner - returns True if winner found, else it returns False
        First player makes a move, then we switch player, then we check for winner
        If there are no piles left that means other player took the last one and the player that is on the move won"""
        counter = 0
        for pile in self.piles:
            if pile == 0:
                counter += 1
        if counter == len(self.piles):
            self.winner = self.player
            return True
        return False

    def make_move(self, action):
        """Makes move and switches player"""
        if self.winner == -1:
            (i, j) = action  # take j coins from i-th pile
            if i < 0 or i > len(self.piles):
                print("ILLEGAL MOVE: Wrong pile index.")
                return
            if self.piles[i] < j:
                print(f"ILLEGAL MOVE: pile {i + 1} has only {self.piles[i]} objects.")
                return
            self.piles[i] -= j
            self.switch_player()
            self.check_for_winner()
        else:
            raise Exception("Winner already determined")

    # ----------------------------------------------------------------------------------
    # ---------- minimax_1   ----------------------------------

    def evaluate(self, nim_instance):
        # pozitivno stevilo dobro za igralca 0
        # negativno stevilo dobro za igralca 1
        # 0 nevtralno

        if nim_instance.winner != -1:
            return (nim_instance.winner * 2) - 1

        non_empty_pile_cnt = 0
        for p in nim_instance.piles:
            if p == 0:
                continue
            non_empty_pile_cnt += 1

        # ce je liho stevilo, je pozicija ugodna za igralca, ki je na vrsti
        eval_result = (non_empty_pile_cnt % 2) == 1

        # normiramo glede na igralca, ki je na vrsti
        if nim_instance.player == 1:
            eval_result *= -1

        return eval_result

    def minimax_play(self, depth, printing=True):
        """ Makes best move selected by minmay algorithm."""
        result = self.minimax(depth, copy.deepcopy(self), self.player, -1e10, 1e10)
        if printing:
            print(f"Minimax izbere : {result[1][0] + 1} {result[1][1]}. preprican? {result[0]}")
        self.make_move(result[1])

    def minimax(self, depth, tmp_nim, maxing_player, alpha, beta):
        """ Runs minmax algorithm on a copy of a game and finds the best move.
        Returns [best_result, move/action]"""
        possible_moves = tmp_nim.possible_actions()
        maximize = maxing_player == tmp_nim.player
        best_eval = 1e10 * (1 + -2 * maximize)
        best_move = None

        for move in possible_moves:
            nim_moved = copy.deepcopy(tmp_nim)
            nim_moved.make_move(move)

            if depth == 0 or nim_moved.winner != -1:
                move_eval = self.evaluate(nim_moved)
            else:
                move_eval = self.minimax(depth - 1, nim_moved, maxing_player, alpha, beta)[0]

            if maximize:
                if move_eval > best_eval:
                    best_eval = move_eval
                    best_move = move

                    alpha = max(alpha, best_eval)
                    if beta <= alpha:
                        break
            else:
                if move_eval < best_eval:
                    best_eval = move_eval
                    best_move = move

                    beta = min(beta, best_eval)
                    if beta <= alpha:
                        break

        return [best_eval, best_move]


if __name__ == "__main__":
    play_in_console_vs_minimax()
    # play_in_console()
