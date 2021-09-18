from collections import deque
from random import shuffle, random
import numpy as np
from functools import reduce

from numpy.lib.function_base import place

cards = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]


class Card:
    def __init__(self, value):
        self.value = value

    def sameAs(self, otherCard):
        if otherCard is None:
            return False
        return self.value == otherCard.value


class Player:
    def __init__(self, name: str):
        self.name = name
        self.slapping_skill = random()
        self.relative_slapping_skill = None
        self.hand = Hand()


class Deck:
    def __init__(self):
        self.cards = deque([Card(value) for value in cards * 4])

    def shuffle(self):
        shuffle(self.cards)

    def deal_one(self):
        return self.cards.pop()

    def has_cards(self):
        return len(self.cards) > 0


class Hand:
    def __init__(self):
        self.cards = deque()

    def get_length(self):
        return len(self.cards)

    def pick_up_cards(self, cards: deque):
        self.cards.extendleft(cards)

    def accept_card(self, card: Card):
        self.cards.appendleft(card)

    def draw(self):
        return self.cards.pop()


class Stack:
    def __init__(self):
        self.cards = deque()
        self.lastFaceCardOwner = None
        self.countdown = 0

    def add(self, card: Card):
        self.cards.append(card)

    def get_top_2(self):
        if len(self.cards) == 1:
            return [None, self.cards[-1]]
        elif len(self.cards) == 0:
            return [None, None]

        return [self.cards[ind] for ind in [-2, -1]]


class Game:
    def __init__(self, players: list):
        self.players = players
        self.deck = Deck()
        self.stack = Stack()
        self.turn = 0

        slapping_skill_sum = sum([p.slapping_skill for p in self.players])

        for p in self.players:
            p.relative_slapping_skill = p.slapping_skill / slapping_skill_sum

        self.slapping_prob_cutoffs = np.cumsum(
            [p.relative_slapping_skill for p in self.players]
        )

    def shuffle_and_deal(self):
        self.deck.shuffle()

        while self.deck.has_cards():
            for player in self.players:
                if not self.deck.has_cards():
                    break
                player.hand.accept_card(self.deck.deal_one())

        for player in self.players:
            print("%s: %d cards" % (player.name, len(player.hand.cards)))

    def getSlapWinner(self):
        rand = random()

        winner = 0
        for prob in self.slapping_prob_cutoffs:
            if rand > prob:
                winner += 1

        return self.players[winner]

    def playTurn(self):
        faceCard = False

        if self.stack.countdown == 0:
            [secondUnder, firstUnder] = self.stack.get_top_2()
            drawnCard = self.players[self.turn].hand.draw()
            self.stack.add(drawnCard)

            if drawnCard.sameAs(secondUnder) or drawnCard.sameAs(firstUnder):
                slapWinner = self.getSlapWinner()
                slapWinner.hand.pick_up_cards(self.stack.cards)
                self.turn = self.players.index(slapWinner)
                return
        else:
            while not faceCard:
                # Get last two cards
                [secondUnder, firstUnder] = self.stack.get_top_2()
                # Player draws card onto stack
                drawnCard = self.players[self.turn].hand.draw()
                self.stack.add(drawnCard)

                if drawnCard.sameAs(secondUnder) or drawnCard.sameAs(
                    firstUnder
                ):
                    slapWinner = self.getSlapWinner()
                    slapWinner.hand.pick_up_cards(self.stack)
                    self.turn = self.players.index(slapWinner)
                    return

                # Handle main game logic
                faceCardValues = {"J": 1, "Q": 2, "K": 3, "A": 4}

                if drawnCard.value in list(faceCardValues.keys()):
                    faceCard = True
                    self.stack.lastFaceCardOwner = self.turn
                    self.stack.countdown = faceCardValues[drawnCard.value]

                    if self.turn < len(self.players) - 1:
                        self.turn += 1
                    else:
                        self.turn = 0
                else:
                    if self.stack.countdown == 1:
                        self.players[
                            self.stack.lastFaceCardOwner
                        ].hand.pick_up_cards(self.stack)
                        self.turn = self.stack.lastFaceCardOwner
                        return

                    self.stack.countdown -= 1

    def printStatus(self):
        for player in self.players:
            print("%s: %d cards" % (player.name, len(player.hand.cards)))
