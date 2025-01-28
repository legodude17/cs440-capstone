from board import Step
from game import PlayerBase
import random

class RandomPlayer(PlayerBase):
  """
  A player that makes random moves
  """
  argcount = 0
  name = "RandomPlayer"
  def choose_step(self) -> Step | None:
    # 5% of the time, end the turn early
    if self.board.state.left < 4 and random.random() < 0.05:
      return None
    moves = list(self.board.possible_steps())
    if len(moves) == 0:
      # If we have no moves, end our turn
      return None
    return random.choice(moves)
