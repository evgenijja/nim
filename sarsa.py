from nim import *
from qlearning import *
from auxillary import *
import random


class SarsaAlgorithm:
    def __init__(self, alpha, gamma, epsilon, smart=False):
        self.alpha = alpha
        self.epsilon = epsilon
        self.gamma = gamma
        self.Q_values = dict()
        self.smart = smart

    def choose_action(self, state, epsilon_greedy=True):
        """In a state with possible actions in that state - chooses best action"""

        game = Nim(state)
        possible_actions = game.possible_actions()
        highest_q_value = None
        best_action = None

        if epsilon_greedy and random.random() < self.epsilon:
            best_action = random.choice(possible_actions)
        else:
            for action in possible_actions:
                action_value = self.Q_values[(tuple(state), action)] if (tuple(state), action) in self.Q_values else 0
                if highest_q_value is None or action_value > highest_q_value:
                    highest_q_value = action_value
                    best_action = action
        return best_action

    def update_model(self, old_state, action, reward):

        if (tuple(old_state), action) in self.Q_values:
            old_Q = self.Q_values[(tuple(old_state), action)]  # q value for old state and action made
        else:
            old_Q = 0

        # new_state = []
        # (i, j) = action
        # for k in range(len(old_state)):
        #     if k != i:
        #         new_state.append(old_state[k])
        #     else:
        #         new_state.append(old_state[k] - j)

        # new_action = self.choose_action(new_state, epsilon_greedy=False)
        # if new_action != 0 and new_action is not None:
        #     new_state = switch_state(new_state, new_action)

        # if (tuple(new_state), new_action) in self.Q_values:
        #     new_Q = self.Q_values[(tuple(new_state), new_action)]  # q value for old state and action made
        # else:
        #     new_Q = 0

        new_state = switch_state(old_state, action)
        if self.smart:
            new_action = make_smart_move(new_state)
        else:
            new_action = self.choose_action(new_state, epsilon_greedy=False)
        # new_action = self.choose_action(new_state, epsilon_greedy=False) 

        if new_action != 0 and new_action != None:

            new_new_state = switch_state(new_state, new_action)
            game = Nim(new_new_state)
            possible_actions = game.possible_actions()
            if possible_actions == []:
                new_Q = 0
            else:
                # namesto da iščemo max spet naredimo epsilon greedy
                new_new_action = self.choose_action(new_new_state, epsilon_greedy=True) 
                if (tuple(new_new_state), new_new_action) in self.Q_values:
                    new_Q = self.Q_values[(tuple(new_new_state), new_new_action)]
                else:
                    new_Q = 0
        else:
            new_Q = 0

        # k = reward + self.epsilon * new_Q
        k = reward + self.gamma * new_Q
        self.Q_values[(tuple(old_state), action)] = old_Q + self.alpha * (k - old_Q)


# algorithm = SarsaAlgorithm(0.5, 0.8)
# train_model(10000, algorithm)
# print(play(algorithm))
# print(random_opponent(100, algorithm))
