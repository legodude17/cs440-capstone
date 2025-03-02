import cProfile
import pstats

# cProfile.run("import testGame", filename="profile.info")

stats = pstats.Stats("profile.info")
stats.strip_dirs()
stats.sort_stats('tottime')
stats.print_stats(.1)
