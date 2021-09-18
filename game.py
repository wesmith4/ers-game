from src.objects import *

players = [Player(name) for name in ["Bob", "Ted", "Lisa"]]

game = Game(players)
game.shuffle_and_deal()

for i in range(30):
    game.playTurn()

game.printStatus()
