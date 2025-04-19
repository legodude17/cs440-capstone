from minimax_moves import get_score
from board import Board, Step

inf = float("inf")

def minimax(board: Board, depth: int, player: int, subset: float = 1):
  bestValue = -inf
  bestStep = None

  for step in board.possible_steps(1 - subset):
    board.do_step(step)
    value = minimax_internal(board, depth - 1, player, subset, inf, -inf)
    if value > bestValue:
      bestValue = value
      bestStep = step
    board.undo_step()

  return (bestStep, bestValue)

def minimax_internal(board: Board, depth: int, player: int, subset: float, alpha: float, beta: float) -> float:
  if depth == 0 or board.state.end:
    if not board.state.end and board.state.left != 4:
      board.finish_turn()
    return get_score(board, player) * (1 + 0.0001 * depth)
  
  if board.state.left == 0:
    board.finish_turn()
    return -minimax_internal(board, depth, player, subset, -beta, -alpha)
  
  bestValue = -inf

  if board.state.left < 4:
    board.finish_turn()
    value = -minimax_internal(board, depth - 1, player, subset, -beta, -alpha)
    if bestValue < value:
      bestValue = value
    if alpha < value:
      alpha = value
      if alpha >= beta:
        return bestValue
    board.undo()

  for step in board.possible_steps(1 - subset):
    board.do_step(step)
    value = minimax_internal(board, depth - 1, player, subset, alpha, beta)

    if bestValue < value:
      bestValue = value
    if alpha < value:
      alpha = value
      if alpha >= beta:
        return bestValue
      
    board.undo_step()
      
  return bestValue
