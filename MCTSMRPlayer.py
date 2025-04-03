from MCTSPlayer import BaseMCTSPlayer, Node
from minimax import minimax

class MCTSMRPlayer(BaseMCTSPlayer):
  name = "MCTSMRPlayer"

  depth = 1 # Minimax depth to use, should probably make this an argument
  subset = 0.1 # Fraction of all possible steps to use at each level of minimax

  def simulate(self, node: Node):
    """
    Simulate a node by running random games and tracking who wins
    """
    reward = 0
    for _ in range(self.rollout):
      self.stats.rollouts += 1
      self.board.decode(node.boardState)
      while not self.board.state.end:
        self.board.do_move(minimax(self.board, self.depth, self.board.state.player, self.subset))

      if self.board.state.player == self.color:
        # If we win, the reward is 1
        reward += 1
      else:
        # If we lose, the "reward" is -1
        reward -= 1
    
    return reward
