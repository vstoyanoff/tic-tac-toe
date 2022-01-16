from game import Game
from player import Player

p1 = Player("p1", is_human=True)
p2 = Player("p2", policy_file="no_file")
game = Game(player_1=p1, player_2=p2)

game.play()
