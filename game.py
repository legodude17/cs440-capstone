import time
from board import Board, COLORS, Step, Move, RANKS, StateException

class StatsBase:
  """
  Holds stats of the bots
  """
  wins: int = 0 # The number of times the bot won a game
  losses: int = 0 # The number of times the bot lost a game
  games: int = 0 # The number of games the bot has played
  time: float = 0 # Total amount of time spent calculating
  turns: int = 0 # Total amount of turns the bot took
  steps: int = 0 # Total amount of steps the bot played

class PlayerBase:
  """
  Abstract class representing a player of Arimaa
  """
  argcount: int # The number of arguments this player needs
  board: Board # The board the player is playing on
  color: int # The color of the player, gold or silver
  stats: StatsBase # The stats of this player
  statsType: type[StatsBase] = StatsBase
  name: str = "PlayerBase" # The name of the player
  args: list
  argnames: list[str]

  def __init__(self, *args) -> None:
    # Default name is ClassName(args)
    self.name = self.__class__.name
    self.args = list(args)
    if len(args) > 0:
      self.name += "(" + ", ".join(args) + ")"
    else:
      self.name += "()"
    self.board = Board()
    self.stats = self.__class__.statsType()

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
    move = []
    for _ in range(4):
      self.board.decode(boardState)
      step = self.choose_step()
      if step == None:
        break
      move.append(step)
      self.board.do_step(step)
      boardState = self.board.encode()
    return tuple(move)
  
  def get_initial(self) -> list[list[int]]:
    return [
      [RANKS.RABBIT, RANKS.RABBIT, RANKS.RABBIT, RANKS.RABBIT,
        RANKS.RABBIT, RANKS.RABBIT, RANKS.RABBIT, RANKS.RABBIT],
      [RANKS.HORSE, RANKS.CAT, RANKS.DOG, RANKS.CAMEL,
        RANKS.ELEPHANT, RANKS.DOG, RANKS.CAT, RANKS.HORSE]
    ]
  
  def get_stats(self) -> dict:
    stats = dict(name=self.name, type=self.__class__.name)
    for i in range(self.__class__.argcount):
      stats[self.__class__.argnames[i]] = self.args[i]
    stats.update(self.stats.__dict__)
    return stats

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
    player.stats.turns += 1
    start = time.time()
    move = player.choose_move(self.board.encode())
    player.stats.time += time.time() - start
    player.stats.steps += len(move)
    try:
      self.board.do_move(move)
    except StateException as e:
      print("Invalid move from", player.name, e, ":", self.board.move_str(move))

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
    for player in self.players:
      player.stats.games += 1
    winner = self.players[self.board.state.player]
    loser = self.players[1 - self.board.state.player]
    winner.stats.wins += 1
    loser.stats.losses += 1
    return self.board.state.player

if __name__ == "__main__":
  # When run directly, do a game between the given two players
  import sys
  import importlib
  import os
  import json
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
  if not os.access("stats", os.R_OK):
    os.mkdir("stats")
  i = 1
  while os.access("stats/game" + str(i) + ".json", os.W_OK):
    i += 1
  with open("stats/game" + str(i) + ".json", "w") as file:
    json.dump([player.get_stats() for player in game.players], file)
  print("Wrote game stats to", "stats/game" + str(i) + ".json")

