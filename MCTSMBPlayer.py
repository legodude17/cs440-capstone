from MCTSPlayer import Node
from MCTSSolverPlayer import MCTSSolverPlayer
from minimax_steps import minimax_internal

inf = float("inf")

class MCTSMBPlayer(MCTSSolverPlayer):
  name = "MCTSMBPlayer"

  depth = 4
  subset = 1

  def check_children(self, node: Node, val: int) -> bool:
    self.board.decode(node.boardState)
    result = minimax_internal(self.board, self.depth, self.color, self.subset, inf, -inf)
    return result == val
