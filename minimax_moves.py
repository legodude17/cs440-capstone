from util import chance
from board import Board, Move, StateException

inf = float("inf")

def minimax(board: Board, depth: int, player: int, subset: float = 1) -> Move:
  """
  Implementation of the Negamax variant of Minimax.
  Used for MCTS-MR, MCTS-MS, and MCTS-MB.
  This version does not use an evaluation function,
  so it simply looks for forced wins and losses.
  If no forced win is found, it simply randomly picks from moves that aren't forced losses.
  """
  bestValue = -inf
  bestMove = None
  num = 1
  for move in board.possible_moves(1 - subset):
    value = minimax_internal(board, depth - 1, player, subset, inf, -inf)
    num += 1
    if value > bestValue or (value == bestValue and chance(1 / num)):
      bestValue = value
      bestMove = move

  if bestMove is None:
    raise StateException("Minimax did not get any possible moves")
  
  return bestMove
  
def minimax_internal(board: Board, depth: int, player: int, subset: float, alpha: float, beta: float) -> float:
  if depth == 0 or board.state.end:
    return get_score(board, player) * (1 + 0.001 * depth)
  
  bestValue = -inf

  for move in board.possible_moves(1 - subset):
    value = -minimax_internal(board, depth - 1, player, subset, -beta, -alpha)

    if bestValue < value:
      bestValue = value
    if alpha < value:
      alpha = value
      if alpha >= beta:
        break

  return bestValue
  
def get_score(board: Board, player: int) -> float:
  """
  Scoring without an evaluation function just means 1000 = win, -1000 = loss, 0 = anything else
  """
  if not board.state.end:
    return 0
  if board.state.player == player:
    return 1000
  else:
    return -1000
