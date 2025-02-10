from typing import Tuple
from game import Game, PlayerBase
from board import COLORS

class Tournament:
  """
  Represents a Round-Robin Arimaa Tournament
  """
  rounds: int # The number of rounds to play
  players: list[PlayerBase] # The players
  wins: list[int] # The number of wins each player gets

  def __init__(self, rounds: int, *players: PlayerBase) -> None:
    self.rounds = rounds
    self.players = list(players)
    self.wins = []
    for _ in range(len(players)):
      self.wins.append(0)

  def __call__(self) -> None:
    """
    Run the tournament
    """
    games = 0
    for _ in range(self.rounds):
      for i in range(len(self.players)):
        for j in range(len(self.players)):
          if i == j: # Players can't play against themselves
            continue
          player1 = self.players[i]
          player2 = self.players[j]
          print(f"{player1.name} vs. {player2.name}:")
          game = Game(player1, player2)
          winner = game.play(False)
          print(f"  {(player1 if winner == COLORS.GOLD else player2).name} wins!")
          self.wins[i if winner == COLORS.GOLD else j] += 1
          games += 1

    print()
    print(f"{games} games, results:")
    for i in range(len(self.wins)):
      print(f"  {self.players[i].name}: {self.wins[i]} wins ({self.wins[i] / games * 100:.2f})")


if __name__ == "__main__":
  # When ran directly, runs a tournament for the given number of rounds using all the given players
  import sys
  import importlib
  import os
  import json
  rounds = int(sys.argv[1])
  args = sys.argv[2:]
  players = []
  i = 0
  while i < len(args):
    className = args[i]
    i += 1
    module = importlib.import_module(className)
    PlayerClass = module.__getattribute__(className)
    playerArgs = []
    for _ in range(PlayerClass.argcount):
      playerArgs.append(args[i])
      i += 1
    players.append(PlayerClass(*playerArgs))

  Tournament(rounds, *players)()
  if not os.access("stats", os.R_OK):
    os.mkdir("stats")
  i = 1
  while os.access("stats/game" + str(i) + ".json", os.W_OK):
    i += 1
  with open("stats/game" + str(i) + ".json", "w") as file:
    json.dump([player.get_stats() for player in players], file)
  print("Wrote stats to", "stats/game" + str(i) + ".json")
