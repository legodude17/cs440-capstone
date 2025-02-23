import sys
from game import StatsBase
import json
import importlib

def read_stats(file: str) -> list[StatsBase]:
  with open(file, "r") as f:
    data = json.load(f)
  stats = []
  for item in data:
    dataType = importlib.import_module(item["type"]).__getattribute__(item["type"])
    statsType = dataType.statsType
    stat = statsType(item["name"])
    stat.__dict__.update(item)
    stats.append(stat)
  return stats

def print_stats(args: list[str]):
  for stats in read_stats(args[0]):
    stats.print()

if __name__ == "__main__":
  # Eventually there'll be more functions here, so here's an easy way to run the given function
  print(eval(sys.argv[1])(sys.argv[2:]))
