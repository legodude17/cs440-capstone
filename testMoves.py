from board import Board, RankChars, COLORS

with open("best_initial.txt") as f:
  text = f.readlines()
initial = [[[RankChars.index(c) for c in line[:8]], [RankChars.index(c) for c in line[8:-1]]] for line in text]

board = Board()
board.place_initial(COLORS.GOLD, initial[COLORS.GOLD])
board.place_initial(COLORS.SILVER, initial[COLORS.SILVER])

print(len(list(board.possible_moves())))
