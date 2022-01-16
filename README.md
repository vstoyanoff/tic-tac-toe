# Tic Tac Toe

An attempt to create an algorithm to teach a non-human player to play tic-tac-toe as efficient as possible.

## Requirements
- python
- poetry
- venv

## Usage

First run `poetry install` and then `poetry shell` to get a shell in the virtual environment provided by poetry.

The program itself has 2 interfaces:
1. Train mode
1. Play mode

### Train

If you want to play against the computer you should probably first train it using the provided interface in the `Game` class. 
```
from game import Game
from player import Player

# Init 2 computer players to play against each other
p1 = Player(name="player_1")
p2 = Player(name="player_2")

# Init a game
game = Game(player_1=p1, player_2=p2)
game.train()
```
This will run a 100 rounds of training producing 2 policy (how to play) files for `p1` and `p2` namely `player_1_policy` and `player_2_policy`

There is a predefined `train.py` script which produces 6 policy files each with different algorithm settings for the player.

### Play

In play mode you can play against other human player or against a computer

```
from game import Game
from player import Player

# Init 2 computer players to play against each other
p1 = Player(name="human_player_1", is_human=True)
p2 = Player(name="player_2", policy_file="player_2_policy")

# Init game and play
game = Game(player_1=p1, player_2=p2)
game.play()
```

There is a `tictactoe.py` file with this code so you can modify it and have fun :)