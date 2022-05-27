from nim import *
from qlearning import *
from sarsa import *
import time
from auxillary import *

# =============================== FUNCTIONS FOR PLAYING AGAINST EACHOTHER =================================================


def qlearn_vs_sarsa(n,  alg1, alg2, generated_piles, optimal_actions=False):
    """Qlearning and SARSA play against each-other."""
    
    wins = {"Q-learning" : 0, "SARSA" : 0}
    ratios_qlearning, ratios_sarsa = [], []
    for i in range(n):
        counter_q, counter_s = [0,0], [0,0] # [num optimal moves made, num all times when optimal move was possible]
        # generated_piles = generate_piles(5,10)
        game = Nim(generated_piles)
        # train_model(num_trainings, alg1, piles=generated_piles)
        # train_model(num_trainings, alg2, piles=generated_piles)

        qlearn = random.randint(0, 1)
        while game.winner == -1:
            if game.player == qlearn:
                state = game.piles.copy()
                action = alg1.choose_action(state, epsilon_greedy=False)
                opt = make_smart_move(state) # pogleda če obstaja kak pameten premik
                val = check_optimal(state, action) # pogleda če je bil ta premik pameten
                if opt != None:
                    counter_q[0] += 1
                if val != None:
                    if val:
                        counter_q[1] += 1
            else:
                state = game.piles.copy()
                action = alg2.choose_action(state, epsilon_greedy=False)
                opt = make_smart_move(state) # pogleda če obstaja kak pameten premik
                val = check_optimal(state, action) # pogleda če je bil ta premik pameten
                if opt != None:
                    counter_s[0] += 1
                if val != None:
                    if val:
                        counter_s[1] += 1
            if action != 0:
                game.make_move(action)
            else:
                print(game.check_for_winner())

            if game.winner != -1:
                if counter_q[0] != 0:
                    ratios_qlearning.append([counter_q[1],counter_q[0]])
                else:
                    ratios_qlearning.append([0,0])
                if counter_s[0] != 0:
                    ratios_sarsa.append([counter_s[1],counter_s[0]])
                else:
                    ratios_sarsa.append([0,0])
                if game.winner == qlearn:
                    wins["Q-learning"] += 1
                else:
                    wins["SARSA"] += 1
    if optimal_actions:
        print(wins)
        return (ratios_qlearning, ratios_sarsa)
    return wins

# print(qlearn_vs_sarsa(20))

def alg_vs_minimax(algorithm, n, num_trainings, optimal_moves=False):
    """Minimax plays against specified algorithm - Qlearning or SARSA."""

    wins = {"Other algorithm" : 0, "Minimax" : 0}
    ratios_alg, ratios_minimax = [], []
    for i in range(n):
        counter_alg, counter_m = [0,0],[0,0]
        piles = generate_piles(5,10)
        alg = train_model(num_trainings, algorithm, piles)
        nim = Nim(piles)

        # randomly choose which player minimax is
        minimax = random.randint(0, 1)
        while not nim.check_for_winner():
            if minimax == nim.player:
                
                state1 = nim.piles.copy()
                # poteza algoritma
                start = time.time()
                nim.minimax_play(4, printing=False)
                end = time.time()
                t = end-start
                # times.append(t)
                state2 = nim.piles.copy()

                action = recognize_action(state1, state2)

                opt = make_smart_move(state1) # pogleda če obstaja kak pameten premik
                val = check_optimal(state1, action) # pogleda če je bil ta premik pameten

                if opt != None:
                    counter_m[0] += 1
                if val != None:
                    if val:
                        counter_m[1] += 1
            else:
                state = nim.piles.copy()
                action = alg.choose_action(state, epsilon_greedy=False)
                opt = make_smart_move(state) # pogleda če obstaja kak pameten premik
                val = check_optimal(state, action) # pogleda če je bil ta premik pameten
                if opt != None:
                    counter_alg[0] += 1
                if val != None:
                    if val:
                        counter_alg[1] += 1
                if action != 0:
                    nim.make_move(action) 
        ratios_alg.append(counter_alg)
        ratios_minimax.append(counter_m)     
        if nim.winner == minimax:
            wins["Minimax"] += 1
        else:
            wins["Other algorithm"] += 1
    if optimal_moves:
        print(wins)
        return (ratios_alg, ratios_minimax)
    return wins

# alg_vs_minimax(Qlearning(0.5, 0.5,0.8), 10)
# alg_vs_minimax(SarsaAlgorithm(0.5, 0.8), 10)


# ==================================== RANDOM OPPONENT =============================================

def random_opponent(n, algorithm, p, optimal_moves=False):
    """Play against random opponent n times and count wins.
    Algorithm is either Qlearning or SARSA"""
    
    # algorithm = train_model(num_trainings, alg, piles=p)

    wins = {"ai" : 0, "random opponent" : 0}
    ratios = []
    for i in range(n):
        optimal_moves_made, optimal_moves_possible = 0,0
        opponent = random.randint(0, 1)
        game = Nim(p)

        while game.winner == -1:
            possible_actions = game.possible_actions()
            if game.player == opponent:
                action = random.choice(possible_actions)

            else:
                state = game.piles.copy()
                action = algorithm.choose_action(state, epsilon_greedy=False)

                                # if optimal_moves:
                opt = make_smart_move(state) # pogleda če obstaja kak pameten premik
                val = check_optimal(state, action) # pogleda če je bil ta premik pameten

                # print(state, action, opt)

                if opt != None:
                    optimal_moves_possible += 1
                if val != None:
                    if val:
                        optimal_moves_made += 1

            if action != 0:
                game.make_move(action)
            else:
                print(game.check_for_winner())

            if game.winner != -1:
                ratios.append([optimal_moves_possible, optimal_moves_made])
                if game.winner == opponent:
                    wins["random opponent"] += 1
                else:
                    wins["ai"] += 1
    if optimal_moves:
        print(wins)
        return ratios
    return wins

def recognize_action(state1, state2):
    """Given 2 states it finds the action that was taken between them"""
    for i in range(len(state1)):
        if state1[i] != state2[i]:
            action = (i, abs(state1[i] - state2[i]))
    return action


def random_opponent_minimax(n, piles, depth, timing=False, optimal_moves=False):
    """Minimax plays against a random opponent."""

    times = []
    wins = {"Random opponent" : 0, "Minimax" : 0}
    ratios = []
    for i in range(n):
        optimal_moves_made, optimal_moves_possible = 0,0
        nim = Nim(piles)

        # randomly choose which player minimax is
        minimax = random.randint(0, 1)
        while not nim.check_for_winner():
            if minimax == nim.player:
                state1 = nim.piles.copy()
                # poteza algoritma
                start = time.time()
                nim.minimax_play(depth, printing=False)
                end = time.time()
                t = end-start
                times.append(t)
                state2 = nim.piles.copy()

                action = recognize_action(state1, state2)

                opt = make_smart_move(state1) # pogleda če obstaja kak pameten premik
                val = check_optimal(state1, action) # pogleda če je bil ta premik pameten

                if opt != None:
                    optimal_moves_possible += 1
                if val != None:
                    if val:
                        optimal_moves_made += 1

            else:
                possible_actions = nim.possible_actions()
                action = random.choice(possible_actions)
                nim.make_move(action)     

        ratios.append([optimal_moves_possible,optimal_moves_made])
        if nim.winner == minimax:
            wins["Minimax"] += 1
        else:
            wins["Random opponent"] += 1

    if optimal_moves:
        print(wins)
        return ratios

    if timing:
        print(wins)
        avg_time = sum(times) / len(times)
        return times

    return wins

# ==================================== SMART OPPONENT ==============================================

def smart_opponent(n, algorithm, piles, optimal_moves=False):
    """Play against a smart opponent n times and count wins.
    Algorithm is either Qlearning or SARSA
    If optimal_moves then the algorithm also return the ration of optimal moves made when they were possible"""
    
    # algorithm = train_model(num_train, alg, piles=piles)

    # optimal_moves_made, optimal_moves_possible = 0,0
    ratios = []
    # print("new game!")
    # print(piles)
    wins = {"ai" : 0, "smart opponent" : 0}
    for i in range(n):
        optimal_moves_made, optimal_moves_possible = 0,0
        opponent = 1 # mora bit drugi na vrsti če ne bo vsakič zmagal
        game = Nim(piles)
        while game.winner == -1:
            state = game.piles.copy()
            if game.player == opponent:
                action = make_smart_move(state)
                if action == None:
                    # if there's no smart move chose randomly
                    possible_actions = game.possible_actions()
                    action = random.choice(possible_actions)
                    
            else:
                
                action = algorithm.choose_action(state, epsilon_greedy=False)
                # if optimal_moves:
                opt = make_smart_move(state) # pogleda če obstaja kak pameten premik
                val = check_optimal(state, action) # pogleda če je bil ta premik pameten

                # print(state, action, opt)

                if opt != None:
                    optimal_moves_possible += 1
                if val != None:
                    if val:
                        optimal_moves_made += 1

            if action != 0:
                game.make_move(action)
            else:
                print(game.check_for_winner())
            if game.winner != -1:
                ratios.append([optimal_moves_possible,optimal_moves_made])
                if game.winner == opponent:
                    wins["smart opponent"] += 1
                else:                    wins["ai"] += 1
            
    if optimal_moves:
        print(wins)
        return ratios
    return wins

def smart_opponent_minimax(n, piles=generate_piles(5,10), optimal_moves=False):
    """Minimax plays against a smart opponent."""

    ratios = []
    wins = {"Smart opponent" : 0, "Minimax" : 0}
    for i in range(n):
        optimal_moves_made, optimal_moves_possible = 0,0
        nim = Nim(piles)

        # randomly choose which player minimax is
        minimax = 0
        while not nim.check_for_winner():
            if minimax == nim.player:
                # poteza algoritma
                state1 = nim.piles.copy()
                # poteza algoritma
                start = time.time()
                nim.minimax_play(4, printing=False)
                end = time.time()
                t = end-start
                # times.append(t)
                state2 = nim.piles.copy()

                action = recognize_action(state1, state2)

                opt = make_smart_move(state1) # pogleda če obstaja kak pameten premik
                val = check_optimal(state1, action) # pogleda če je bil ta premik pameten

                # print(state, action, opt)

                if opt != None:
                    optimal_moves_possible += 1
                if val != None:
                    if val:
                        optimal_moves_made += 1
            else:
                state = nim.piles.copy()
                
                action = make_smart_move(state)
                if action == None:
                    # if there's no smart move chose randomly
                    possible_actions = nim.possible_actions()
                    action = random.choice(possible_actions)
                nim.make_move(action)      

        ratios.append([optimal_moves_possible,optimal_moves_made])
        if nim.winner == minimax:
            wins["Minimax"] += 1
        else:
            wins["Smart opponent"] += 1

    if optimal_moves:
        print(wins)
        return ratios
    return wins

# smart_opponent(10, Qlearning(0.5, 1, 0.2), optimal_moves=True)