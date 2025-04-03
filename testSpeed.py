import cProfile
import pstats
import sys

if len(sys.argv) > 1:
  cProfile.run("import " + sys.argv[1], filename="profile.info")

stats = pstats.Stats("profile.info")
stats.strip_dirs()
stats.sort_stats('tottime')
stats.print_stats(.1)
