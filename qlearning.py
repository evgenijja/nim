
from nim import *
import random
import numpy as np
from auxillary import *

def switch_state(state, action):
    """Switches state accordind to action."""
    new_state = []
    for i in range(len(state)):
        if i != action[0]:
            new_state.append(state[i])
        else:
            new_state.append(state[i] - action[1])
    return new_state


class Qlearning():

    def __init__(self, alpha, gamma, epsilon, smart=False):
        """Initialize the process with parameters and empty Q-table 
        (all states and actions at the beginning are considered to have value 0)"""
        self.alpha = alpha
        self.epsilon = epsilon
        self.gamma = gamma
        self.Qtable = dict() 
        self.smart = smart


    def choose_action(self, state, epsilon_greedy=True):
        """In a state with possible actions in that state - chooses an action.
        If epsilon_greedy is true that means with probability self.epsilon we choose a random action,
        otherwise we choose the action with maximal reward."""

        game = Nim(state)
        possible_actions = game.possible_actions()

        highest_q_value = None
        best_action = None

        # For epsilon_greedy method: 
        # generate a random number between 0 and 1 - with self.epsilon probability it will be lower that self.epsilon
        r = random.random()
        if epsilon_greedy and r < self.epsilon: # epsilon greedy method
            best_action = random.choice(possible_actions)

        else: 
            # highest possible Q value - read from the table
            for a in possible_actions:
                if (tuple(state), a) in self.Qtable:
                    a_value = self.Qtable[(tuple(state), a)]
                else: 
                    # if it's not in the dictionary it has starting value 0
                    a_value = 0
                if highest_q_value == None or a_value > highest_q_value:
                    highest_q_value = a_value
                    best_action = a
        return best_action

    def update_model(self, old_state, action, reward):
        """Old state, action made and reward recieved from that action used to update Q learning model according to the bellman equation"""
        if (tuple(old_state), action) in self.Qtable:
            old_q = self.Qtable[(tuple(old_state), action)] # q value for old state and action made
        else:
            old_q = 0

        new_state = switch_state(old_state, action)
        if self.smart:
            new_action = make_smart_move(new_state)
        else:
            new_action = self.choose_action(new_state, epsilon_greedy=False)
        if new_action != 0 and new_action != None:
            new_new_state = switch_state(new_state, new_action)
            game = Nim(new_new_state)
            possible_actions = game.possible_actions()
            if possible_actions == []:
                best_reward = 0
            else:
                best_reward = None
                for a in possible_actions:
                    if (tuple(new_new_state), a) in self.Qtable:
                        a_value = self.Qtable[(tuple(new_new_state), a)]
                    else:
                        a_value = 0
                    if  best_reward == None or a_value > best_reward:
                        best_reward = a_value
        else:
            best_reward = 0
        # update q value according to bellman equation
        new_q = old_q + self.alpha * ((reward + self.gamma * best_reward) - old_q)
        self.Qtable[(tuple(old_state), action)] = new_q


        

# ========================= TRAINING THE MODEL ===================================================

# pri taki začetni postavitvi dobim slabše rezultate ampak to je logično, ker če je random prvi 
# in se mu posreči da izbere ravno (1,2) (za kar je 1/3 možnosti) bo seveda zmagal
# piles = [0,3,0]


def train_model(n, algorithm, piles):
    """Training the model n times with algorithm (for e/xample Qlearning()). 
    We train the model with the same game all the time?"""

    for i in range(n):
        game = Nim(piles)
        # last move made by either player
        moves = {0 : [None, None], 1 : [None, None]} # (state, action)

        play = True
        while play: 
            
            current_state = game.piles.copy()
            action = algorithm.choose_action(current_state)

            moves[game.player][0] = current_state 
            moves[game.player][1] = action 

            game.make_move(action) # switches player 
            if game.winner != -1:
                if moves[game.player][0] is not None:
                    algorithm.update_model(moves[game.player][0], moves[game.player][1], 1)
                    algorithm.update_model(current_state, action, -1)
                    play = False
                else: # meaning only 2 moves were made
                    algorithm.update_model(current_state, action, -1)
                    play = False

            elif game.winner == -1: 
                if moves[game.player][0] is not None:
                    algorithm.update_model(moves[game.player][0], moves[game.player][1], 0)
                
    return algorithm


# ===================== FUNCTIONS FOR PLAYING =======================================

def play(algorithm=Qlearning(0.5, 0.1, 0.1), human=None, piles=generate_piles(10,10)):
    """Human is either 0 or 1"""
    if human == None:
        human = random.randint(0, 1) # randomly chose who if human is player 1 or 0
    game = Nim(piles)

    while game.winner == -1:
        possible_actions = game.possible_actions()
        print(game.piles)
        if game.player == human:
            print("your turn!")
            pile = int(input("Choose pile: "))
            count = int(input("Choose # coins: "))

            action = (pile, count)
            if action not in possible_actions:
                raise Exception("Not a possible action!")  
                return
        else:
            print("AI's turn!")
            state = game.piles.copy()
            action = algorithm.choose_action(state, epsilon_greedy=False)

        if action != 0:
            game.make_move(action)
        else:
            print(game.check_for_winner())

        if game.winner != -1:

            if game.winner == human:
                w = "HUMAN"
            else:
                w = "AI"
    return "Winner is: " + w

alg = Qlearning(0.5, 0.1, 0.1)
# train_model(10000, alg)

# play(train_model(10000, Qlearning(0.1, 0.5, 0.1, smart=True), piles=[3, 3, 5, 7]), piles=[3,3,5,7]) 
        
