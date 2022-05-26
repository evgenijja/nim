from nim import *
from qlearning import *

# ================================= USEFUL FUNCTIONS FOR SMART OPPONENT ==========================================

def switch_state(state, action):
    """Switches state accordind to action."""
    new_state = []
    for i in range(len(state)):
        if i != action[0]:
            new_state.append(state[i])
        else:
            new_state.append(state[i] - action[1])
    return new_state


def nimsum(piles):
    """Returns the nim-sum of the state."""

    # convert numbers to binary
    binary, maxlen = [], 0
    for pile in piles:
        num = bin(pile)[2:] # odbijemo prefix
        binary.append(num) 
        if len(num) > maxlen:
            maxlen = len(num)

    # make them all the same length
    new_binary = []
    for elt in binary:
        if len(elt) < maxlen:
            new_elt = (maxlen - len(elt))*"0" + elt
            new_binary.append(new_elt)
        else:
            new_binary.append(elt)
    
    sum = 0
    for i in range(maxlen):
        current_sum = 0
        for elt in new_binary:
            rev = elt[::-1]
            current_sum += int(rev[i])
        sum += (current_sum % 2)
    
    return sum


def check_optimal(state, action):
    """Checks if the action taken in the given state is optimal."""
    # če imamo samo eno mesto kjer je več kot en kovanec bomo morali posebej obravnavati
    ones, not_ones, where = 0, 0, dict()
    for i in range(len(state)):
        if state[i] == 1:
            ones += 1
        elif state[i] > 1:
            not_ones += 1
            where[i] = state[i] # za vsako mesto si zapomni število

    if nimsum(state) == 0 or sum(state) == 1:
        # v tem primeru ni optimalne akcije in ne štejemo 
        return None
    
    # če imamo poseben primer ga moramo posebej obravnavat
    if not_ones == 1:
        key = list(where.keys())[0] # key = mesto 
        n = where[key] # n je koliko coinsev je na tem mestu
        if ones % 2 == 0:
            optimal_action = (key, n-1)
        else:
            optimal_action = (key, n)
        return optimal_action == action

    else:
        # v tem primeru gledamo nim sum po narejeni akciji
        new_state = switch_state(state, action)
        nim = nimsum(new_state)
        return nim == 0

def make_smart_move(state):
    """Returns a smart move so that the nim sum of new state is zero 
    (except at the end where there is a twist)"""
    nim = Nim(state)
    possible_actions = nim.possible_actions()
    for action in possible_actions:
        val = check_optimal(state, action)
        if val:
            return action
    return None