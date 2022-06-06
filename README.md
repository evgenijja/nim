## Different approaches to the solution of the Nim game

Authors: Evgenija Burger, Barbara Lipnik, Saša Ošlaj

Comparison of reinforcement learning algorithms on Nim game.

Algorithms compared:
* Minimax with alpha beta pruning
* Q-learning
* SARSA

Files and what they contain:
* ```nim.py``` includes class Nim we used for all algorithms and the implementation of minimax algorithm
* ```qlearning.py``` and ```sarsa.py``` include the implementations of Q-learning and SARSA algorithms as well as the function for training
* ```play.py``` includes functions for playing against eachother or against a random opponent
* ```auxillary.py``` includes useful functions for the third part of the comparison - functions fro calculating nim sum and making winning moves
* ```comparison.ipynb``` and ```better_comparison.ipynb``` include most of the analysis and comparisons we did
