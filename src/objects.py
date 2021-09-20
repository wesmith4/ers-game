from collections import deque
from random import shuffle, random
import numpy as np
import pandas as pd
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

    def empty(self):
        self.cards.clear()


class Game:
    def __init__(self, players: list):
        self.players = players
        self.deck = Deck()
        self.stack = Stack()
        self.turn = 0
        self.cumulativeTurns = 0
        self.faceCardValues = {"A": 4, "K": 3, "Q": 2, "J": 1}
        self.log = []

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
        self.logStatus()

    def getSlapWinner(self):
        rand = random()

        winner = 0
        for prob in self.slapping_prob_cutoffs:
            if rand > prob:
                winner += 1

        return self.players[winner]

    def logStatus(self):
        status = {"turn": self.cumulativeTurns}
        for playerNum in range(len(self.players)):
            status["player%s" % playerNum] = self.players[
                playerNum
            ].hand.get_length()
        self.log.append(status)

    def playTurn(self):
        faceCard = False
        self.cumulativeTurns += 1

        while not faceCard:

            [secondUnder, firstUnder] = self.stack.get_top_2()

            # Determine if this is right person to draw
            foundPlayer = False
            while not foundPlayer:
                if self.players[self.turn].hand.cards.__len__() == 0:
                    print("Player %d ran out of cards" % self.turn)
                    if self.turn < self.players.__len__() - 1:
                        self.turn += 1
                    else:
                        self.turn = 0
                else:
                    foundPlayer = True

            drawnCard = self.players[self.turn].hand.draw()
            self.stack.add(drawnCard)

            # Detect slap situation
            if drawnCard.sameAs(secondUnder) or drawnCard.sameAs(firstUnder):
                slapWinner = self.getSlapWinner()
                slapWinner.hand.pick_up_cards(self.stack.cards)
                self.stack.empty()
                self.turn = self.players.index(slapWinner)
                print("%s won a slap!" % slapWinner.name)
                self.logStatus()
                return

            if drawnCard.value in list(self.faceCardValues.keys()):
                faceCard = True
                self.stack.lastFaceCardOwner = self.turn
                self.stack.countdown = self.faceCardValues[drawnCard.value]
                if self.turn < len(self.players) - 1:
                    self.turn += 1
                else:
                    self.turn = 0
                self.logStatus()
                return
            else:
                if self.stack.countdown == 0:
                    if self.turn < len(self.players) - 1:
                        self.turn += 1
                    else:
                        self.turn = 0
                    self.logStatus()
                    return
                elif self.stack.countdown == 1:
                    self.players[
                        self.stack.lastFaceCardOwner
                    ].hand.pick_up_cards(self.stack.cards)
                    self.stack.empty()
                    self.turn = self.stack.lastFaceCardOwner
                    print(
                        "Player %d picks up cards by countdown"
                        % self.stack.lastFaceCardOwner
                    )
                    self.logStatus()
                    return
                else:
                    self.stack.countdown -= 1

    def printStatus(self):
        for player in self.players:
            print("%s: %d cards" % (player.name, len(player.hand.cards)))
        print("Cards in stack: %d" % self.stack.cards.__len__())
        print(
            "Total cards: %d"
            % sum(
                [len(player.hand.cards) for player in self.players],
                self.stack.cards.__len__(),
            )
        )
        print("Cumulative Turns: %d\n" % self.cumulativeTurns)

    def play(self):
        while all([player.hand.get_length() < 52 for player in self.players]):
            self.playTurn()
            if self.cumulativeTurns > 100000:
                break

    def getResults(self):
        return pd.DataFrame(self.log)
