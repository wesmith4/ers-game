from collections import deque
from random import shuffle, random


ranks = {
    "A": 13,
    "2": 1,
    "3": 2,
    "4": 3,
    "5": 4,
    "6": 5,
    "7": 6,
    "8": 7,
    "9": 8,
    "10": 9,
    "J": 10,
    "Q": 11,
    "K": 12,
}


class Card:
    def __init__(self, value):
        self.value = value
        self.rank = ranks[value]


class Player:
    def __init__(self, name: str):
        self.name = name
        self.slapping_skill = random()


class Deck:
    def __init__(self):
        self.cards = deque([Card(value) for value in list(ranks.keys()) * 4])

    def shuffle(self):
        shuffle(self.cards)


class Hand:
    def __init__(self):
        self.cards = deque()

    def get_length(self):
        return len(self.cards)

    def pick_up_cards(self, cards: deque):
        self.cards.appendleft(cards)

    def draw(self):
        return self.cards.pop()
