from board import Step, Piece, RankChars
from game import PlayerBase

class HumanPlayer(PlayerBase):
  """
  A player that is controlled by asking the human for moves
  """
  argcount = 0
  name = "HumanPlayer"
  def choose_step(self) -> Step | None:
    self.board.print()
    # Keep asking for steps until a valid one is given
    while True:
      print("Enter your next step in standard notation:", end=" ")
      res = input().split(" ")
      # The human can just press enter to finish their turn
      if len(res) == 0 or len(res[0]) == 0:
        return None
      push = None
      if len(res) == 2:
        push = res[1]
      try:
        step = self.board.parse_step(res[0], push)
        return step
      except:
        print("Invalid step, please try again.")
        
  def get_initial(self) -> list[list[Piece]]:
    print("Choose starting setup:")
    print("  Enter the order you want them to start in, starting with the front line, from left right.")
    text = input()
    initial = [[], []]
    initial[0] = [RankChars.index(c) for c in text[:8]]
    initial[1] = [RankChars.index(c) for c in text[8:]]
    return initial

