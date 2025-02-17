from board import Move
from game import PlayerBase
import random

class RandomPlayer(PlayerBase):
  """
  A player that makes random moves
  """
  argcount = 0
  name = "RandomPlayer"
  def choose_move(self, boardState: str) -> Move:
    self.board.decode(boardState)
    moves = list(self.board.possible_moves())
    return random.choice(moves)
