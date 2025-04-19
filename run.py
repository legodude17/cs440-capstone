
from board import Board
from importlib import import_module

boardState = input("Enter board state:")
board = Board()
board.decode(boardState)

impt = input("Enter player name:")
module = import_module(impt)
PlayerClass = module.__getattribute__(impt)
args = []
for i in range(PlayerClass.argcount):
  arg = input("Enter value for " + PlayerClass.argnames[i] + ":")
  args.append(arg)
player = PlayerClass(*args)
player.color = board.state.player

move = player.choose_move(boardState)
print("Chosen move:", board.move_str(move))
