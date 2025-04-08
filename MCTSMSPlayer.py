
from MCTSPlayer import Node
from MCTSSolverPlayer import MCTSSolverPlayer
from minimax_steps import minimax_internal

infi = 2**-32
inff = float("inf")

class MCTSMSPlayer(MCTSSolverPlayer):
  name = "MCTSMSPlayer"

  depth = 4 # Depth of the minimax search to use
  subset = 0.5 # Fraction of all nodes to consider for minimax search as a decimal

  def select(self, node: Node):
    path = []
    while True:
      path.append(node)
      self.stats.explored += 1
      if len(node.children) == 0:
        return path
      for child in node.children:
        if len(child.children) == 0:
          self.stats.explored += 1
          path.append(child)
          return path
      if node.N >= self.visitThreshold:
        for child in node.children:
          self.board.decode(child.boardState)
          value = minimax_internal(self.board, self.depth, self.color, self.subset, inff, -inff)
          if value == inff:
            self.stats.explored += 1
            child.Q = infi
            path.append(child)
            return path
          if value == -inff:
            self.stats.explored += 1
            child.Q = -infi
            path.append(child)
            return path
      node = max(node.children, key=self.uct)
