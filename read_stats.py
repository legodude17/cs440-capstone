import sys
from MCTSPlayer import MCTSStats
from game import StatsBase
import json
import importlib

def read_stats(file: str) -> list[StatsBase]:
  try:
    with open(file, "r") as f:
      data = json.load(f)
    stats = []
    for item in data:
      dataType = importlib.import_module(item["type"]).__getattribute__(item["type"])
      statsType = dataType.statsType
      stat = statsType(item["name"], item["type"])
      stat.__dict__.update(item)
      stats.append(stat)
    return stats
  except:
    print("Error reading " + file)
    return []

def print_stats(args: list[str]):
  for stats in read_stats(args[0]):
    stats.print()

def create_graphs(args: list[str]):
  import matplotlib.pyplot as plt
  stats: dict[str, list[StatsBase]] = dict()
  for file in args:
    for player in read_stats(file):
      if player.type in stats:
        stats[player.type].append(player)
      else:
        stats[player.type] = [player]

  fig = plt.figure()
  ax = fig.subplots()
  ax.set_title("Execution time (s) vs Average Iterations per Turn")
  ax.set_ylabel("Average Iterations per Turn")
  ax.set_xlabel("Execution time (s)")
  for key, players in stats.items():
    xs = []
    ys = []
    for player in players:
      xs.append(player.__dict__["execTime"])
      ys.append(player.iterations / player.turns) # type: ignore
    ax.plot(xs, ys, label=key)
  ax.legend()
  fig.savefig("iterPlot.png")

  fig = plt.figure()
  ax = fig.subplots()
  ax.set_title("Execution time (s) vs Average Rollouts per Turn")
  ax.set_ylabel("Average Rollouts per Turn")
  ax.set_xlabel("Execution time (s)")
  for key, players in stats.items():
    xs = []
    ys = []
    for player in players:
      xs.append(player.__dict__["execTime"])
      ys.append(player.rollouts / player.turns) # type: ignore
    ax.plot(xs, ys, label=key)
  ax.legend()
  fig.savefig("rolloutPlot.png")

def total_time(args: list[str]):
  time = 0
  for file in args:
    for stats in read_stats(file):
      time += stats.time

  return time

def total_games(args: list[str]):
  games = 0
  for file in args:
    for stats in read_stats(file):
      games += stats.games

  return games / 2 # Each game is counted twice

def time_per_game(args: list[str]):
  time = 0
  games = 0
  for file in args:
    for stats in read_stats(file):
      time += stats.time
      games += stats.games

  games /= 2 # Each game is counted twice because it involves 2 players

  return time / games

if __name__ == "__main__":
  # Eventually there'll be more functions here, so here's an easy way to run the given function
  print(eval(sys.argv[1])(sys.argv[2:]))
