from board import Move, StateException, Step, Piece, RankChars
from game import PlayerBase, StatsBase
from typing import TypeVar
import time
import math
import random

Self = TypeVar("Self", bound="Node")

class Node:
  boardState: str # The state of the board at this node
  children: list[Self] # type: ignore
  parent: Self | None # type: ignore
  move: Move | None # The move that led to this node
  N: int # The number of times this node has been visited
  Q: int # The total reward of this node and all it's children

  def __init__(self, boardState: str, parent: Self | None, move: Move | None) -> None: # type: ignore
    self.children = []
    self.N = 0
    self.Q = 0
    self.boardState = boardState
    self.parent = parent
    self.move = move

class MCTSStats(StatsBase):
  """
  Stats for the Monte-Carlo Tree Search
  """
  iterations: int = 0 # Total number of iterations conducted
  explored: int = 0 # Total number of nodes explored (considered for selection)
  created: int = 0 # Total number of nodes created
  rollouts: int = 0 # Total number of rollouts conducted

class MCTSPlayer(PlayerBase):
  """
  Monte-Carlo Tree Search Player
  """
  # Takes 2 arguments:
  argcount = 2
  #   1) The amount of time in seconds to think about each move
  execTime: int
  #   2) The number of times to simulate a random game to determine a moves win rate
  rollout: int
  # The first increases skill as it increases, the second one usually does the same.
  # However, increasing the second increases the time each leaf takes to process,
  # so increasing it without the first may reduce skill instead.
 
  name = "MCTSPlayer"
  argnames = ["execTime", "rollout"]
  statsType = MCTSStats
  stats: MCTSStats
  
  def __init__(self, *args) -> None:
    super().__init__(*args)
    self._nextRoot = None
    self.execTime = int(args[0])
    self.rollout = int(args[1])

  def choose_move(self, boardState: str) -> Move:
    startTime = time.time() # Keep track of execution time to limit calculation
    root = Node(boardState, None, None)
    while time.time() - startTime < self.execTime:
      # 1 iteration of MCTS:
      #   Select -> Expand -> Simulate -> Backpropagate
      self.stats.iterations += 1
      path = self.select(root)
      leaf = path[-1]
      self.expand(leaf)
      reward = self.simulate(leaf)
      self.backup(path, reward)

    # Find the best move by examining the root's children
    bestNode = max(root.children, key=self.score)
    if bestNode.move == None:
      raise StateException("Best move is to pass, which is impossible")
    else:
      return bestNode.move
  
  def expand(self, node: Node):
    """
    Expand a node by adding children for each of the possible moves at that states
    """
    if len(node.children) > 0:
      return
    self.board.decode(node.boardState)
    for move in self.board.possible_moves():
      self.stats.created += 1
      node.children.append(Node(self.board.encode(), node, move))

  def select(self, node: Node):
    """
    Select a node to explore this iteration, by choosing children by uct until we find an unexplored node
    """
    path = []
    while True:
      self.stats.explored += 1
      path.append(node)
      if len(node.children) == 0:
        return path
      for child in node.children:
        if len(child.children) == 0:
          self.stats.explored += 1
          path.append(child)
          return path
      node = max(node.children, key=self.uct)

  def simulate(self, node: Node):
    """
    Simulate a node by running random games and tracking who wins
    """
    reward = 0
    for _ in range(self.rollout):
      self.stats.rollouts += 1
      self.board.decode(node.boardState)
      while not self.board.state.end:
        moves = list(self.board.possible_moves())
        self.board.do_move(random.choice(moves))

      if self.board.state.player == self.color:
        # If we win, the reward is 1
        reward += 1
      else:
        # If we lose, the "reward" is -1
        reward -= 1
    return reward
  
  def backup(self, path: list[Node], reward: int):
    """
    Propogate the reward back up the tree, increasing the N and Q values appropriately
    """
    for node in reversed(path):
      node.N += 1
      node.Q += reward

  @staticmethod
  def uct(node: Node):
    """
    Upper Confidence Bounds for Trees, a formula used to balance exploration and exploitation
    We always select the child with the highest value of this
    """
    if node.parent == None:
      return float("inf")
    return node.Q / node.N + math.sqrt(2) * math.sqrt(math.log(node.parent.N) / node.N)
  
  @staticmethod
  def score(node: Node):
    """
    The score of a node is it's average reward, used to select the best move
    """
    if node.N == 0:
      return float("-inf")
    return node.Q / node.N
  
  def get_initial(self) -> list[list[Piece]]:
    # We use the game data reader to determine the best initial setup by winrate and use that
    with open("best_initial.txt") as f:
      text = f.readlines()[self.color]
    initial = [[], []]
    initial[0] = [RankChars.index(c) for c in text[:8]]
    initial[1] = [RankChars.index(c) for c in text[8:-1]]
    return initial
