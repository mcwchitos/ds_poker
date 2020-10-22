from enum import Enum
from random import shuffle
from celery import *
import operator


class SUIT(Enum):
    HEARTS = 1
    SPADES = 2
    DIAMONDS = 3
    CLUBS = 4


class VALUE(Enum):
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5
    SIX = 6
    SEVEN = 7
    EIGHT = 8
    NINE = 9
    TEN = 10
    JACK = 11
    QUEEN = 12
    KING = 13
    ACE = 14


class Card:

    def __init__(self, SUIT=SUIT.HEARTS, VALUE=VALUE.TWO):
        self.SUIT = SUIT
        self.VALUE = VALUE


class DeckOfCards(Card):
    NUM_OF_CARDS = 52

    def __init__(self):
        super().__init__()
        self.deck = []

    def setUpDeck(self):
        for suit in [e.value for e in SUIT]:
            for value in [e.value for e in VALUE]:
                self.deck.append(Card(suit, value))
        shuffle(self.deck)


class DealCards(DeckOfCards):

    def __init__(self):
        super().__init__()
        self.playersHands = []
        self.playerCoins = [1000, 1000, 1000, 1000]
        self.bets = [0, 0, 0, 0]
        self.bank = 0
        self.order = 0

    def Deal(self):
        self.setUpDeck()
        self.getHands()
        # self.evaluateHands()

    def CoinsRotate(self, n):
        self.playerCoins = (self.playerCoins[n: len(self.playerCoins)] + self.playerCoins[0:n])

    def HandsRotate(self, n):
        self.playersHands = (self.playersHands[n: len(self.playersHands)] + self.playersHands[0:n])

    def BetsRotate(self, n):
        self.bets = (self.bets[n: len(self.bets)] + self.bets[0:n])

    def getHands(self):
        otherPlayer0Hand = []
        otherPlayer1Hand = []
        otherPlayer2Hand = []
        otherPlayer3Hand = []
        for i in range(self.order, self.order + 5):
            otherPlayer0Hand.append(self.deck[4 * i])
            otherPlayer1Hand.append(self.deck[4 * i + 1])
            otherPlayer2Hand.append(self.deck[4 * i + 2])
            otherPlayer3Hand.append(self.deck[4 * i + 3])
        self.order += 20
        self.playersHands.append(otherPlayer0Hand)
        self.playersHands.append(otherPlayer1Hand)
        self.playersHands.append(otherPlayer2Hand)
        self.playersHands.append(otherPlayer3Hand)

    def bet(self, player, amount):
        self.playerCoins[player] -= amount
        self.bets[player] += amount
        self.bank += amount

    def getCards(self, player):
        return self.playersHands[player]

    def getCard(self, player,  i):
        self.playersHands[player][i] = self.deck[self.order]
        # self.otherPlayer0Hand[i] = self.deck[self.order]
        self.order += 1

    def DisplayMyCards(self, player):
        print('------ your hand ------')
        for card in self.playersHands[player]:
            if card.SUIT == SUIT.HEARTS.value:
                print('\u2665', card.VALUE)
            elif card.SUIT == SUIT.SPADES.value:
                print('\u2660', card.VALUE)
            elif card.SUIT == SUIT.CLUBS.value:
                print('\u2663', card.VALUE)
            elif card.SUIT == SUIT.DIAMONDS.value:
                print('\u2666', card.VALUE)

    def DisplayCards(self):
        for hand in self.playersHands:
            print('---------------------------')
            for card in hand:
                if card.SUIT == SUIT.HEARTS.value:
                    print('\u2665', card.VALUE)
                elif card.SUIT == SUIT.SPADES.value:
                    print('\u2660', card.VALUE)
                elif card.SUIT == SUIT.CLUBS.value:
                    print('\u2663', card.VALUE)
                elif card.SUIT == SUIT.DIAMONDS.value:
                    print('\u2666', card.VALUE)

    def evaluateHands(self):
        sortedHands = []
        for hand in self.playersHands:
            sortedHands = sortCel(hand)

        handEvals = crtEvals(sortedHands)


        finalHands = []
        for eval in handEvals:
            finalHands.append(eval.EvaluateHand())

        if finalHands[0] > finalHands[1] and finalHands[0] > finalHands[2] and finalHands[0] > finalHands[3]:
            return 1
        elif finalHands[1] > finalHands[0] and finalHands[1] > finalHands[2] and finalHands[1] > finalHands[3]:
            return 2
        elif finalHands[2] > finalHands[0] and finalHands[2] > finalHands[1] and finalHands[2] > finalHands[3]:
            return 3
        elif finalHands[3] > finalHands[0] and finalHands[3] > finalHands[2] and finalHands[3] > finalHands[1]:
            return 4
        else:
            if handEvals[0].handValue.Total > handEvals[1].handValue.Total and handEvals[0].handValue.Total > handEvals[2].handValue.Total and handEvals[0].handValue.Total > handEvals[3].handValue.Total:
                return 1
            elif handEvals[1].handValue.Total > handEvals[0].handValue.Total and handEvals[1].handValue.Total > handEvals[2].handValue.Total and handEvals[1].handValue.Total > handEvals[3].handValue.Total:
                return 2
            elif handEvals[2].handValue.Total > handEvals[0].handValue.Total and handEvals[2].handValue.Total > handEvals[1].handValue.Total and handEvals[2].handValue.Total > handEvals[3].handValue.Total:
                return 3
            elif handEvals[3].handValue.Total > handEvals[0].handValue.Total and handEvals[3].handValue.Total > handEvals[2].handValue.Total and handEvals[3].handValue.Total > handEvals[1].handValue.Total:
                return 4
            elif handEvals[0].handValue.HighCard > handEvals[1].handValue.HighCard and handEvals[0].handValue.HighCard > handEvals[2].handValue.HighCard and handEvals[0].handValue.HighCard > handEvals[3].handValue.HighCard:
                return 1
            elif handEvals[1].handValue.HighCard > handEvals[0].handValue.HighCard and handEvals[1].handValue.HighCard > handEvals[2].handValue.HighCard and handEvals[1].handValue.HighCard > handEvals[3].handValue.HighCard:
                return 2
            elif handEvals[2].handValue.HighCard > handEvals[0].handValue.HighCard and handEvals[2].handValue.HighCard > handEvals[1].handValue.HighCard and handEvals[2].handValue.HighCard > handEvals[3].handValue.HighCard:
                return 3
            elif handEvals[3].handValue.HighCard > handEvals[0].handValue.HighCard and handEvals[3].handValue.HighCard > handEvals[2].handValue.HighCard and handEvals[3].handValue.HighCard > handEvals[1].handValue.HighCard:
                return 4


class Hand(Enum):
    Nothing = 0
    OnePair = 1
    TwoPairs = 3
    ThreeKind = 10
    Straight = 15
    Flush = 30
    FullHouse = 50
    FourKind = 100
    RoyalFlush = 200


class HandValue:
    def __init__(self):
        self.Total = 0
        self.HighCard = 0


class HandEvaluator(Card):

    def __init__(self, sortedHand):
        super().__init__()
        self.heartsSum = 0
        self.diamondSum = 0
        self.clubSum = 0
        self.spadesSum = 0
        self.cards = []
        self.Cards = sortedHand
        self.handValue = HandValue()
        for card in self.Cards:
            self.cards.append(card)

    def EvaluateHand(self):
        self.getNumberOfSuit()
        if self.RoyalFlush():
            return Hand.RoyalFlush.value
        elif self.FourOfKind():
            return Hand.FourKind.value
        elif self.FullHouse():
            return Hand.FullHouse.value
        elif self.Flush():
            return Hand.Flush.value
        elif self.Straight():
            return Hand.Straight.value
        elif self.ThreeOfKind():
            return Hand.ThreeKind.value
        elif self.TwoPairs():
            return Hand.TwoPairs.value
        elif self.OnePair():
            return Hand.OnePair.value

        self.handValue.HighCard = self.cards[4].VALUE
        return Hand.Nothing.value

    def getNumberOfSuit(self):
        for element in self.Cards:
            if element.SUIT == SUIT.HEARTS:
                self.heartsSum += 1
            elif element.SUIT == SUIT.DIAMONDS:
                self.diamondSum += 1
            elif element.SUIT == SUIT.CLUBS:
                self.clubSum += 1
            elif element.SUIT == SUIT.SPADES:
                self.spadesSum += 1

    def RoyalFlush(self):
        if self.heartsSum == 5 or self.diamondSum == 5 or self.clubSum == 5 or self.spadesSum == 5:
            if self.cards[0].VALUE == VALUE.TEN and self.cards[1].VALUE == VALUE.JACK and self.cards[2].VALUE == VALUE.QUEEN and self.cards[3].VALUE == VALUE.KING and self.cards[4].VALUE == VALUE.ACE:
                return True
        return False

    def FourOfKind(self):
        if self.cards[0].VALUE == self.cards[1].VALUE and self.cards[0].VALUE == self.cards[2].VALUE and self.cards[0].VALUE == self.cards[3].VALUE:
            self.handValue.Total = self.cards[1].VALUE * 4
            self.handValue.HighCard = self.cards[4].VALUE
            return True
        elif self.cards[1].VALUE == self.cards[2].VALUE and self.cards[1].VALUE == self.cards[3].VALUE and self.cards[
            1].VALUE == self.cards[4].VALUE:
            self.handValue.Total = self.cards[1].VALUE * 4
            self.handValue.HighCard = self.cards[0].VALUE
            return True
        return False

    def FullHouse(self):
        if self.cards[0].VALUE == self.cards[1].VALUE and self.cards[0].VALUE == self.cards[2].VALUE and self.cards[
            3].VALUE == self.cards[4].VALUE or self.cards[0].VALUE == self.cards[1].VALUE and self.cards[2].VALUE == \
                self.cards[3].VALUE and self.cards[2].VALUE == self.cards[4].VALUE:
            self.handValue.Total = self.cards[0].VALUE + self.cards[1].VALUE + self.cards[2].VALUE + self.cards[
                3].VALUE + self.cards[4].VALUE
            return True
        return False

    def Flush(self):
        if self.heartsSum == 5 or self.diamondSum == 5 or self.clubSum == 5 or self.spadesSum == 5:
            self.handValue.Total = self.cards[4].VALUE
            return True
        return False

    def Straight(self):
        if self.cards[0].VALUE + 1 == self.cards[1].VALUE and self.cards[1].VALUE + 1 == self.cards[2].VALUE and \
                self.cards[2].VALUE + 1 == self.cards[3].VALUE and self.cards[3].VALUE + 1 == self.cards[4].VALUE:
            self.handValue.Total = self.cards[4].VALUE
            return True
        return False

    def ThreeOfKind(self):
        if self.cards[0].VALUE == self.cards[1].VALUE and self.cards[0].VALUE == self.cards[2].VALUE or self.cards[1].VALUE == self.cards[2].VALUE and self.cards[1].VALUE == self.cards[3].VALUE:
            self.handValue.Total = self.cards[2].VALUE * 3
            self.handValue.HighCard = self.cards[4].VALUE
            return True
        elif self.cards[2].VALUE == self.cards[3].VALUE and self.cards[2].VALUE == self.cards[4].VALUE:
            self.handValue.Total = self.cards[2].VALUE * 3
            self.handValue.HighCard = self.cards[1].VALUE
            return True
        return False

    def TwoPairs(self):
        if self.cards[0].VALUE == self.cards[1].VALUE and self.cards[2].VALUE == self.cards[3].VALUE:
            self.handValue.Total = self.cards[1].VALUE * 2 + self.cards[3].VALUE * 2
            self.handValue.HighCard = self.cards[4].VALUE
            return True
        elif self.cards[0].VALUE == self.cards[1].VALUE and self.cards[3].VALUE == self.cards[4].VALUE:
            self.handValue.Total = self.cards[1].VALUE * 2 + self.cards[3].VALUE * 2
            self.handValue.HighCard = self.cards[2].VALUE
            return True
        elif self.cards[1].VALUE == self.cards[2].VALUE and self.cards[3].VALUE == self.cards[4].VALUE:
            self.handValue.Total = self.cards[1].VALUE * 2 + self.cards[3].VALUE * 2
            self.handValue.HighCard = self.cards[0].VALUE
            return True
        return False

    def OnePair(self):
        if self.cards[0].VALUE == self.cards[1].VALUE:
            self.handValue.Total = self.cards[0].VALUE * 2
            self.handValue.HighCard = self.cards[4].VALUE
            return True
        elif self.cards[1].VALUE == self.cards[2].VALUE:
            self.handValue.Total = self.cards[1].VALUE * 2
            self.handValue.HighCard = self.cards[4].VALUE
            return True
        elif self.cards[2].VALUE == self.cards[3].VALUE:
            self.handValue.Total = self.cards[2].VALUE * 2
            self.handValue.HighCard = self.cards[4].VALUE
            return True
        elif self.cards[3].VALUE == self.cards[4].VALUE:
            self.handValue.Total = self.cards[3].VALUE * 2
            self.handValue.HighCard = self.cards[2].VALUE
            return True
        return False
