import pandas as pd
from board import Board, COLORS, parse_initial, RankChars
import sys

def standardize_initial(initial: list[str]):
  """
  Create a standard representation of an initial setup
  """
  _, init = parse_initial(initial)
  return "".join(["".join([RankChars[rank] for rank in row]) for row in init])

def find_best_initial():
  """
  Find the best initial setup based on total wins for both gold and silver
  """
  dataG = {}
  dataS = {}
  with pd.read_csv("allgames.txt", usecols=["result", "movelist"], chunksize=1) as reader:
    for item in reader:
      winner = item["result"].item()
      movelist = item["movelist"].item()
      moves = movelist.split("\\n")
      if len(moves) < 2:
        continue
      try:
        initialG = standardize_initial(moves[0].split(" ")[1:])
      except:
        continue
      try:
        initialS = standardize_initial(moves[1].split(" ")[1:])
      except:
        continue
      if winner == "w" or winner == "g":
        data = dataG
        initial = initialG
      elif winner == "b" or winner == "s":
        data = dataS
        initial = initialS
      if not initial in data:
        data[initial] = 1
      else:
        data[initial] += 1
  
  bestG = max(dataG, key=dataG.get) # type: ignore
  bestS = max(dataS, key=dataS.get) # type: ignore
  print("Gold:", bestG, dataG[bestG])
  print("Silver:", bestS, dataS[bestS])
  with open("best_initial.txt", "w") as f:
    f.write(bestG + "\n" + bestS + "\n")
  return bestG, bestS

if __name__ == "__main__":
  # Eventually there'll be more functions here, so here's an easy way to run the given function
  print(eval(sys.argv[1])())
