from lib2to3.pgen2.pgen import generate_grammar
from nim import Nim, generate_piles

game1 = generate_piles(10, 10)
nim1 = Nim(game1)

game2 = [0, 0, 0]
nim2 = Nim(game2)
# print(nim2.check_for_winner())

game3 = [0, 0, 2]
nim3 = Nim(game3)
print(nim3.check_for_winner())
nim3.make_move((2, 2))
print(nim3.check_for_winner())
print(nim3.winner)
print(nim3.make_move((1, 1)))
