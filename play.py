from nim import *
from qlearning import *
from sarsa import *


def qlearn_vs_sarsa(n, alg1=Qlearning(0.6, 0.7, 0.4), alg2=SarsaAlgorithm(0.5, 0.8)):
    """Qlearning and SARSA play against each-other."""
    
    wins = {"Q-learning" : 0, "SARSA" : 0}
    for i in range(n):
        piles = generate_piles(10,10)
        game = Nim(piles)
        train_model(10000, alg1)
        train_model(10000, alg2)

        qlearn = random.randint(0, 1)
        while game.winner == -1:
            if game.player == qlearn:
                state = game.piles.copy()
                action = alg1.choose_action(state, epsilon_greedy=False)
            else:
                state = game.piles.copy()
                action = alg2.choose_action(state, epsilon_greedy=False)
            if action != 0:
                game.make_move(action)
            else:
                print(game.check_for_winner())

            if game.winner != -1:
                if game.winner == qlearn:
                    wins["Q-learning"] += 1
                else:
                    wins["SARSA"] += 1
    return wins

# print(qlearn_vs_sarsa(20))

def alg_vs_minimax(algorithm, n):
    """Minimax plays against specified algorithm - Qlearning or SARSA."""

    wins = {"Other algorithm" : 0, "Minimax" : 0}
    for i in range(n):
        piles = generate_piles(10,10)
        alg = train_model(10000, algorithm)
        nim = Nim(piles)

        # randomly choose which player minimax is
        minimax = random.randint(0, 1)
        while not nim.check_for_winner():
            if minimax == nim.player:
                # poteza algoritma
                nim.minimax_play(4, printing=False)
            else:
                state = nim.piles.copy()
                action = alg.choose_action(state, epsilon_greedy=False)
                if action != 0:
                    nim.make_move(action)      
        if nim.winner == minimax:
            wins["Minimax"] += 1
        else:
            wins["Other algorithm"] += 1
    return wins

# alg_vs_minimax(Qlearning(0.5, 0.5,0.8), 10)
# alg_vs_minimax(SarsaAlgorithm(0.5, 0.8), 10)