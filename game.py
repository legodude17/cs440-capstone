from board import Board, COLORS, Step, Move, Piece, RANKS, piece_to_char, StateException

class PlayerBase:
  """
  Abstract class representing a player of Arimaa
  """
  argcount: int # The number of arguments this player needs
  board: Board # The board the player is playing on
  color: int # The color of the player, gold or silver
  name: str = "PlayerBase" # The name of the player

  def __init__(self, *args) -> None:
    # Default name is ClassName(args)
    self.name = self.__class__.name
    if len(args) > 0:
      self.name += "(" + ", ".join(args) + ")"
    else:
      self.name += "()"
    self.board = Board()

  def choose_step(self) -> Step | None:
    """
    Choose the step to play from the current board
    Must either implement this or choose_move
    Return None to finish turn early
    """
    raise NotImplementedError()
  
  def choose_move(self, boardState: str) -> Move:
    """
    Choose the move to play from the given board
    Default implementation will write the board to the class's board, then call choose_step until either four steps are provided or None is returned
    """
    self.board.decode(boardState)
    step1 = self.choose_step()
    if step1 == None:
      raise StateException("Cannot completely pass the turn!")
    self.board.decode(boardState)
    step2 = self.choose_step()
    if step2 == None:
      return step1,
    self.board.decode(boardState)
    step3 = self.choose_step()
    if step3 == None:
      return step1,step2
    self.board.decode(boardState)
    step4 = self.choose_step()
    if step4 == None:
      return step1,step2,step3
    return step1,step2,step3,step4
  
  def get_initial(self) -> list[list[int]]:
    return [
      [RANKS.RABBIT, RANKS.RABBIT, RANKS.RABBIT, RANKS.RABBIT,
        RANKS.RABBIT, RANKS.RABBIT, RANKS.RABBIT, RANKS.RABBIT],
      [RANKS.HORSE, RANKS.CAT, RANKS.DOG, RANKS.CAMEL,
        RANKS.ELEPHANT, RANKS.DOG, RANKS.CAT, RANKS.HORSE]
    ]

class Game:
  """
  Represents a game of Arimaa between two players
  """
  board: Board
  players: list[PlayerBase]
  
  def __init__(self, player1: PlayerBase, player2: PlayerBase) -> None:
    # Assign the player's colors
    player1.color = COLORS.GOLD
    player2.color = COLORS.SILVER
    self.players = [player1, player2]
    self.board = Board()

  def setup(self):
    """
    Do the board setup for both players
    """
    for i in range(len(self.players)):
      self.board.place_initial(i, self.players[i].get_initial())

  def turn(self):
    """
    Do one turn, which involves a player taking 1-4 steps
    """
    player = self.players[self.board.state.player]
    # Continue taking steps until they run out, the other player's turn starts, or the game ends
    while self.board.state.left > 0 and self.board.state.player == player.color and not self.board.state.end:
      move = player.choose_move(self.board.encode())
      try:
        self.board.do_move(move)
      except StateException as e:
        print("Invalid move from", player, e, ":")
        i = 1
        for step in move:
          print(str(i) + ".", self.board.step_str(step), piece_to_char(self.board[step.oldPos]), "->", piece_to_char(self.board[step.newPos])) # type: ignore
          i += 1

  def play(self, printBoards: bool):
    """
    Play a game until one player wins, optionally printing the board at each turn
    """
    self.setup()
    if printBoards:
      self.board.print()
    while not self.board.state.end:
      self.turn()
      if printBoards:
        self.board.print()
    return self.board.state.player

if __name__ == "__main__":
  # When run directly, do a game between the given two players
  import sys
  import importlib
  if len(sys.argv) < 3:
    print("Error: Need to specific the two player classes")
    exit(1)
  args = sys.argv[1:]
  module = importlib.import_module(args[0])
  Player1Class = module.__getattribute__(args[0])
  n1 = Player1Class.argcount
  module = importlib.import_module(args[n1+1])
  Player2Class = module.__getattribute__(args[n1+1])
  n2 = Player2Class.argcount
  player1 = Player1Class(*args[1:n1+1])
  player2 = Player2Class(*args[n1+2:n1+2+n2+1])
  game = Game(player1, player2)
  game.play(True)
