from board import COLORS
from game import PlayerBase, Game
import time

class Evaluator:
  rounds: int
  player: PlayerBase
  players: list[PlayerBase]
  wins: list[int]
  losses: list[int]

  def __init__(self, rounds: int, player: PlayerBase, *players: PlayerBase) -> None:
    self.rounds = rounds
    self.player = player
    self.players = list(players)
    self.wins = []
    self.losses = []
    for _ in range(len(self.players)):
      self.wins.append(0)
      self.losses.append(0)

  def __call__(self):
    startTime = time.time()
    games = 0
    for _ in range(self.rounds):
      for i in range(len(self.players)):
        opp = self.players[i]
        print(f"{self.player.name} vs. {opp.name}")
        game = Game(self.player, opp)
        winner = game.play(False)
        print(f"  {(self.player if winner == COLORS.GOLD else opp).name} wins!")
        (self.wins if winner == COLORS.GOLD else self.losses)[i] += 1
        games += 1

    elapsedTime = time.time() - startTime
    print()
    print(f"Evaluation of {self.player.name}:")
    for i in range(len(self.players)):
      print(f"  vs. {self.players[i].name}: {self.wins[i]} wins, {self.losses[i]} losses, {self.wins[i] + self.losses[i]} total")
    print(f"Ran {games} games in {elapsedTime}s ({elapsedTime / games}s/game)")

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

  Evaluator(rounds, *players)()
  if not os.access("stats", os.R_OK):
    os.mkdir("stats")
  i = 1
  while os.access("stats/game" + str(i) + ".json", os.W_OK):
    i += 1
  with open("stats/game" + str(i) + ".json", "w") as file:
    json.dump([player.get_stats() for player in players], file)
  print("Wrote stats to", "stats/game" + str(i) + ".json")


