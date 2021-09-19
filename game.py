from src.objects import *

players = [Player(name) for name in ["Bob", "Ted", "Lisa"]]

game = Game(players)
game.shuffle_and_deal()

while all([player.hand.get_length() < 52 for player in game.players]):
    game.playTurn()
    game.printStatus()

game.printStatus()
