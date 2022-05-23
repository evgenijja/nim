
from nim import *
import random
import numpy as np

def switch_state(state, action):
    new_state = []
    for i in range(len(state)):
        if i != action[0]:
            new_state.append(state[i])
        else:
            new_state.append(state[i] - action[1])
    return new_state


class Qlearning():

    def __init__(self, alpha, epsilon):

        self.alpha = alpha
        self.epsilon = epsilon

        # at the beginnign all q values are zero 
        self.Qtable = dict() 


    def choose_action(self, state, epsilon_greedy=True):
        """In a state with possible actions in that state - chooses best action"""

        game = Nim(state)
        possible_actions = game.possible_actions()

        highest_q_value = None
        best_action = None

        r = random.random()
        if epsilon_greedy and r < self.epsilon: # epsilon greedy method
            best_action = random.choice(possible_actions)

        else: # highest possible Q value
            
            for a in possible_actions:
                if (tuple(state), a) in self.Qtable:
                    a_value = self.Qtable[(tuple(state), a)]
                else: # if it's not in the dictionary
                    a_value = 0

                if highest_q_value == None or a_value > highest_q_value:
                    highest_q_value = a_value
                    best_action = a
                
            # print((highest_q_value, best_action))
        return best_action


    def max_reward(self, state):
        game = Nim(state)
        possible_actions = game.possible_actions()

        if possible_actions == []:
            return 0
            # raise Exception("Winner already determined")
        else:
            reward = None
            for a in possible_actions:
                if (tuple(state), a) in self.Qtable:
                    a_value = self.Qtable[(tuple(state), a)]
                else:
                    a_value = 0
                if  reward == None or a_value > reward:
                    reward = a_value

        return reward


    def update_model(self, old_state, action, reward):
        """Old state, action made and reward recieved from that action used to update Q learning model"""

        if (tuple(old_state), action) in self.Qtable:
            old_q = self.Qtable[(tuple(old_state), action)] # q value for old state and action made
        else:
            old_q = 0
        
        new_state = []
        (i, j) = action
        for k in range(len(old_state)):
            if k != i:
                new_state.append(old_state[k])
            else:
                new_state.append(old_state[k] - j)

        # g = Nim(new_state)
        # possible_actions = g.possible_actions()
        new_action = self.choose_action(new_state, epsilon_greedy=False)
        if new_action != 0 and new_action != None:
            new_new_state = switch_state(new_state, new_action)
            best_reward = self.max_reward(new_new_state)
        else:
            best_reward = 0

        new_q = old_q + self.alpha * ((reward + best_reward) - old_q)
        self.Qtable[(tuple(old_state), action)] = new_q




        

# ============================================================================

# piles = generate_piles(10, 10) # todo qlearning mora sprejet začetno stanje al ne?
piles = [5, 5, 5]

def train_model(n, algorithm=Qlearning):
    """Training the model n times with algorithm (for e/xample Qlearning()). 
    We train the model with the same game all the time?"""

    for i in range(n):

        game = Nim(piles)
        
        # last move made by either player
        moves = {0 : [None, None], 1 : [None, None]} # (state, action)

        play = True
        while play: # game.winner == -1:
            

            current_state = game.piles.copy()

            action = algorithm.choose_action(current_state)

            # print((current_state, action))

            if False: #action == 0:
                print("tukej sm NIKOLI")
                play = False
            else:

                moves[game.player][0] = current_state 
                moves[game.player][1] = action 


                game.make_move(action) # switches player 
                new_state = game.piles.copy()

                # print(new_state)

                if game.winner != -1: # and moves[game.player][0] is not None: # if someone won update q values with rewards

                    algorithm.update_model(moves[game.player][0], moves[game.player][1], 1)
                    algorithm.update_model(current_state, action, -1)
                    play = False

                elif game.winner == -1: # and moves[game.player][0] is not None:

                    # algorithm.update_model(current_state, action, 0) # no rewards yet
                    if moves[game.player][0] is not None:
                        algorithm.update_model(moves[game.player][0], moves[game.player][1], 0)
                        
                    # else:
                    #     algorithm.update_model(current_state, action, 0)

                

        # print(algorithm.Qtable)
        # print(moves)
    # print(i)
    return algorithm

def play(algorithm=Qlearning(0.5, 0.1), human=None):

    """Human is either 0 or 1"""
    if human == None:
        human = random.randint(0, 1)
    game = Nim(piles)

    while game.winner == -1:
        # print(game.piles)

        legit = True
        possible_actions = game.possible_actions()
        print(game.piles)
        if game.player == human:
            print("your turn!")
            pile = int(input("Choose pile: "))
            count = int(input("Choose # coins: "))

            action = (pile, count)
            if action not in possible_actions:
                
                raise Exception("Not a possible action!") # todo 
                legit = False
        else:
            print("AI's turn!")
            # possible_actions = game.possible_actions()
            # print(possible_actions)
            state = game.piles.copy()
            action = algorithm.choose_action(state, epsilon_greedy=False)

        if action != 0 and legit == True:
            # print(action)
            game.make_move(action)
        else:
            print(game.check_for_winner())

        if game.winner != -1:

            if game.winner == human:
                w = "HUMAN"
            else:
                w = "AI"
    # print(w)
    return w

alg = Qlearning(0.5, 0.1)
train_model(10000, alg)
# play(alg)


            
# alg.Qtable
# {((5, 5, 5), (0, 1)): 7e-323, ((4, 5, 5), (0, 1)): 6.4e-323, ((3, 5, 5), (0, 1)): 6e-323, ((2, 5, 5), (0, 1)): 5.4e-323, ((1, 5, 5), (0, 1)): 5e-323, ((0, 5, 5), (1, 1)): 4.4e-323, ((0, 4, 5), (1, 1)): 4e-323, ((0, 3, 5), (1, 1)): 3.5e-323, ((0, 2, 5), (1, 1)): 3e-323, ((0, 1, 5), (1, 1)): 2.5e-323, ((0, 0, 5), (2, 1)): 2e-323, ((0, 0, 4), (2, 1)): 1.5e-323, ((0, 0, 3), (2, 1)): 1e-323, ((0, 0, 1), (2, 1)): -1.0, ((0, 0, 2), (2, 1)): 5e-324}


# todo če natreniraš na 10 stolpcev po 10 kovancev lahko potem poženeš na random igri (10, 10)

def random_opponent(n, algorithm):

    """Play against random opponent n times and count wins"""
    wins = {"ai" : 0, "random opponent" : 0}
    for i in range(n):
        opponent = random.randint(0, 1)
        game = Nim(piles)

        while game.winner == -1:
            # print(game.piles)

            legit = True
            possible_actions = game.possible_actions()
            # print(game.piles)
            if game.player == opponent:

                action = random.choice(possible_actions)

            else:

                state = game.piles.copy()
                action = algorithm.choose_action(state, epsilon_greedy=False)

            if action != 0 and legit == True:
                # print(action)
                game.make_move(action)
            else:
                print(game.check_for_winner())

            if game.winner != -1:

                if game.winner == opponent:
                    wins["random opponent"] += 1
                else:
                    wins["ai"] += 1
    # print(w)
    return wins

print(random_opponent(100, alg))