import math
from random import choice
from MCTSPlayer import BaseMCTSPlayer, Node

inf = 2**31

class MCTSSolverPlayer(BaseMCTSPlayer):
  name = "MCTSSolverPlayer"
  visitThreshold = 5 # Parameter for after how many visits to start ignore proven losses, may want to make it an argument

  def select(self, node: Node):
    # If a child has a reward of inf (win), then we don't need to select anything
    # If a child has a reward of -inf (loss), then we decide based on the node's visit count
    # If it is above visitThreshold, we select the normal way, which will never pick -inf nodes
    # If not, we select randomly, we could pick -inf nodes
    # In addition, if a node has a visit count of 1, we check if any children are a win for the moving player
    # If so, the move is immediately declared a win and we stop searching
    # This should skip all rollouts and immediately move to backprop
    path = []
    while True:
      path.append(node)
      self.stats.explored += 1
      if len(node.children) == 0:
        return path
      if node.N == 1:
        win = False
        self.board.decode(node.boardState)
        curPlayer = self.board.state.player
        for child in node.children:
          self.board.decode(node.boardState)
          if self.board.state.end and self.board.state.player == curPlayer:
            win = True
        if win:
          node.Q = inf if curPlayer == self.color else -inf
          return path
      random = False
      for child in node.children:
        if child.Q == -inf and child.N < self.visitThreshold:
          random = True
        if child.Q == inf or len(child.children) == 0:
          self.stats.explored += 1
          path.append(child)
          return path
      if random:
        node = choice(node.children)
      else:
        node = max(node.children, key=self.uct)

  def simulate(self, node: Node):
    self.board.decode(node.boardState)
    if self.board.state.end:
      if self.board.state.player == self.color:
        return inf
      else:
        return -inf
    else:
      return super().simulate(node)
  
  def backup(self, path: list[Node], reward: int):
    prevPlayer = -1
    prevNode: Node = None # type: ignore
    for node in reversed(path):
      curPlayer = node.player
      node.N += 1
      if prevPlayer == -1:
        node.Q += reward
      else:
        if prevNode.Q == inf:
          if prevPlayer == self.color:
            node.Q = inf
          else:
            if self.check_children(node, inf):
              node.Q = -inf
        elif prevNode.Q == -inf:
          if prevPlayer == self.color:
            if self.check_children(node, -inf):
              node.Q = inf
          else:
            node.Q = -inf
        
        if reward != inf and reward != -inf:
          node.Q += reward
      
      prevPlayer = curPlayer
      prevNode = node

  @staticmethod
  def check_children(node: Node, val: int) -> bool:
    for child in node.children:
      if child.Q != val:
        return False
    return True

  @staticmethod
  def score(node: Node):
    """
    The score of a node according to the Secure Child strategy
    """
    if node.N == 0:
      return float("-inf")
    return node.Q + 1/math.sqrt(node.N)
  

