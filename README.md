# Arimaa Bot(s)

> A main arimaa bot and a bunch of supporting infrastructure

The main bot of the project is housed in `MCTSPlayer.py`. It is an Arimaa bot using the Monte-Carlo Tree Search algorithm.

## Best Initial

The MCTS bot starts with the best initial setup by total wins from existing games. This is contained in the file `best_inital.txt`, which is generated by `read_gamedata.py`. If you want to make it anew, here are the steps:

1. Run `python download_gamedata.py`. This will download all the game files from the arimaa website and turn them into one massive file called `allgames.txt`. Warning: It will take a while and use a lot of RAM.
2. Run `python read_gamedata.py find_best_initial`. This will read the `allgames.txt` file and find the best initial setup and write it to `best_initial.txt`. Warning: It will take a while.

## Arguments

The MCTS bot takes two arguments: 1) the allowed time to calculate each step and 2) the number of times to simulate each node to determine it's winrate. Increase them both to increase the difficulty. However, do note that since there are four steps in a move each turn will actually take 4 times longer than the allowed time, as well as some extra for the game logic.

## Examples

To pit a random bot (gold) against a MCTS bot (silver) that takes 1 second to choose a move based on 10 simulations per node: `python game.py RandomPlayer MCTSPlayer 1 10`

To pit yourself (gold) against a random bot (silver): `python game.py HumanPlayer RandomPlayer`

To start a 5 round tournament of 5 random bots: `python 5 tournament.py RandomPlayer RandomPlayer RandomPlayer RandomPlayer RandomPlayer`

To start a 10 round tournament of random bot, a MCTS bot with 1 second based on 1 simulation per node, a MCTS bot with 1 second based on 10 simulations per node, a MCTS bot with 10 seconds based on 1 simulation per node, and a MCTS bot with 10 seconds based on 10 simulations per node: `python tournament.py 10 RandomPlayer MCTSPlayer 1 1 MCTSPlayer 10 1 MCTSPlayer 10 10`

## Files

- `best_initial.txt` contains the best initial moves for gold and silver, calculated by `read_gamedata.py`
- `board.py` contains an implementation of Arimaa
- `download_gamedata.py` downloads all the game data from the Arimaa website and merges it into a giant table called `allgames.txt`
- `game.py` contains the base player class and a simple class that plays a game between two players until one wins
- `HumanPlayer.py` contains a player that asks the user for the moves
- `MCTSPlayer.py` contains a Monte-Carlo Tree Search bot, which is the main product of the project
- `RandomPlayer.py` contains a player that makes random moves
- `read_gamedata.py` contains a script to determine the best initial setups by total wins
- `README.md` is the document you are reading
- `tournament.py` is class that runs a round-robin tournament between an arbitrary number of players

## Next Steps

The main next steps would be making more bots, and I can think of a few interesting ideas for one:

- A minimax bot. This would be interesting as due to the huge branching factor (up to 200,000), it would most likely have to instead use a random subset of nodes. It could be expanded to use a neural network as the evaluator instead of a written function.
- A neural network bot. Basically train a neural network on the game data to predict the next move, then use it as a bot.
- An AlphaZero-style bot that learns via self-play. This would be a lot of work but it'd be theoretically possible to reimplement AlphaZero from the paper but for Arimaa. However, there's no way I could get enough computing power to train it properly (the team behind leela-zero estimates it'd take 1700 years with commercially available hardware).

## Sources

- The [Arimaa Game Rules](http://arimaa.com/arimaa/learn/rules.pdf)
- The [Arimaa Notation Explainer](http://arimaa.com/arimaa/learn/notation.html)
- [leela-zero's readme](https://github.com/leela-zero/leela-zero/blob/next/README.md) (for the estimate of the time to train an AlphaZero-style bot)
- The [Wikipedia page for Monte-Carlo Tree Search](https://en.wikipedia.org/wiki/Monte_Carlo_tree_search) was surprisingly informative
- [wlongxiang/mcts](https://github.com/wlongxiang/mcts/blob/main/monte_carlo_tree_search.py) is an excellent example of how to implement MCTS in python
- A whole bunch of documentation pages for python, pandas, etc.
