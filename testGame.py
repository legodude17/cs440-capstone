import os
import json
from game import Game
from MCTSPlayer import MCTSPlayer

game = Game(MCTSPlayer("1", "1"), MCTSPlayer("5", "3"))
game.play(True)
if not os.access("stats", os.R_OK):
  os.mkdir("stats")
i = 1
while os.access("stats/game" + str(i) + ".json", os.W_OK):
  i += 1
with open("stats/game" + str(i) + ".json", "w") as file:
  json.dump([player.get_stats() for player in game.players], file)
print("Wrote game stats to", "stats/game" + str(i) + ".json")
