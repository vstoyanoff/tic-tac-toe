from game import Game
from player import Player

# First set
v1 = Player("v1")
v2 = Player("v2", random_action_rate=0.2, learning_rate=0.4, decay_gamma=0.8)
game = Game(player_1=v1, player_2=v2)
game.train(rounds=1000)

# Second set
v3 = Player("v3", random_action_rate=0.1, learning_rate=0.1, decay_gamma=0.5)
v4 = Player("v4", random_action_rate=0.4, learning_rate=0.2, decay_gamma=0.3)
game = Game(player_1=v3, player_2=v4)
game.train(rounds=1000)

# Third set
v5 = Player("v5", random_action_rate=0.6, learning_rate=0.7, decay_gamma=0.95)
v6 = Player("v6", random_action_rate=0.05, learning_rate=0.1, decay_gamma=0.95)
game = Game(player_1=v5, player_2=v6)
game.train(rounds=1000)
