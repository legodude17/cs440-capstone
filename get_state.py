from board import Board, RANKS, COLORS
from random import randint

initial = [
      [RANKS.RABBIT, RANKS.RABBIT, RANKS.RABBIT, RANKS.RABBIT,
        RANKS.RABBIT, RANKS.RABBIT, RANKS.RABBIT, RANKS.RABBIT],
      [RANKS.HORSE, RANKS.CAT, RANKS.DOG, RANKS.CAMEL,
        RANKS.ELEPHANT, RANKS.DOG, RANKS.CAT, RANKS.HORSE]
    ]

board = Board()
board.place_initial(COLORS.GOLD, initial)
board.place_initial(COLORS.SILVER, initial)

for _ in range(randint(30, 45)):
  board.do_move(board.random_move())

print(board.encode())
