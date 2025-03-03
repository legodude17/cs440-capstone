import math
from MCTSPlayer import BaseMCTSPlayer, Node

class MCTSSolverPlayer(BaseMCTSPlayer):
  name = "MCTSSolverPlayer"
  inf = float("inf")
  visitThreshold = 20 # Parameter for after how many visits to start ignore proven losses, may want to make it an argument

  def select(self, node: Node):
    # If a child has a reward of inf (win), then we don't need to select anything
    # If a child has a reward of -inf (loss), then we decide based on the node's visit count
    # If it is above visitThreshold, we select the normal way, which will never pick -inf nodes
    # If not, we select randomly, we could pick -inf nodes
    # In addition, if a node has a visit count of 1, we check if any children are a win for the moving player
    # If so, the move is immediately declared a win and we stop searching
    # This should skip all rollouts and immediately move to backprop
    return super().select(node)

  def simulate(self, node: Node):
    # If a child of a node is a win for the player to move, then that node is a win
    # If all children of a node is a loss for the player to move, then that node is a loss
    # Use a reward of inf for a win for us and -inf for a loss for us
    return super().simulate(node)
  
  def backup(self, path: list[Node], reward: int):
    # Reward could be -inf or inf, propogate that too according to the logic above
    return super().backup(path, reward)
  
  @staticmethod
  def score(node: Node):
    """
    The score of a node according to the Secure Child strategy
    """
    if node.N == 0:
      return float("-inf")
    return node.Q + 1/math.sqrt(node.N)
  

