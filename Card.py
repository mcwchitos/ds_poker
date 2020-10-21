from enum import Enum
from random import shuffle
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
        self.otherPlayer0Hand = []
        self.otherPlayer1Hand = []
        self.otherPlayer2Hand = []
        self.otherPlayer3Hand = []
        self.order = 0

    def Deal(self):
        self.setUpDeck()
        self.getHands()
        self.playersHands.append(self.otherPlayer0Hand)
        self.playersHands.append(self.otherPlayer1Hand)
        self.playersHands.append(self.otherPlayer2Hand)
        self.playersHands.append(self.otherPlayer3Hand)


        # self.evaluateHands()

    def getHands(self):
        for i in range(self.order, self.order + 5):
            self.otherPlayer0Hand.append(self.deck[4 * i])
            self.otherPlayer1Hand.append(self.deck[4 * i + 1])
            self.otherPlayer2Hand.append(self.deck[4 * i + 2])
            self.otherPlayer3Hand.append(self.deck[4 * i + 3])
        self.order += 20

    def getCard(self, player,  i):
        self.playersHands[player - 1][i] = self.deck[self.order]
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
            for card in hand:
                print('---------------------------')
                if card.SUIT == SUIT.HEARTS.value:
                    print('\u2665', card.VALUE)
                elif card.SUIT == SUIT.SPADES.value:
                    print('\u2660', card.VALUE)
                elif card.SUIT == SUIT.CLUBS.value:
                    print('\u2663', card.VALUE)
                elif card.SUIT == SUIT.DIAMONDS.value:
                    print('\u2666', card.VALUE)


    def evaluateHands(self):
        sortedMy = sorted(self.otherPlayer0Hand, key=operator.attrgetter('VALUE'))
        sorted1 = sorted(self.otherPlayer1Hand, key=operator.attrgetter('VALUE'))
        sorted2 = sorted(self.otherPlayer2Hand, key=operator.attrgetter('VALUE'))
        sorted3 = sorted(self.otherPlayer3Hand, key=operator.attrgetter('VALUE'))

        myHandEval = HandEvaluator(sortedMy)
        hand1Eval = HandEvaluator(sorted1)
        hand2Eval = HandEvaluator(sorted2)
        hand3Eval = HandEvaluator(sorted3)

        myHand = myHandEval.EvaluateHand()
        hand1 = hand1Eval.EvaluateHand()
        hand2 = hand2Eval.EvaluateHand()
        hand3 = hand3Eval.EvaluateHand()

        if myHand > hand1 and myHand > hand2 and myHand > hand3:
            print('you win!')
        elif hand1 > myHand and hand1 > hand2 and hand1 > hand3:
            print('playe 1 wins')
        elif hand2 > myHand and hand2 > hand1 and hand2 > hand3:
            print('playe 2 wins')
        elif hand3 > myHand and hand3 > hand2 and hand3 > hand1:
            print('playe 3 wins')
        else:
            if myHandEval.handValue.Total > hand1Eval.handValue.Total and myHandEval.handValue.Total > hand2Eval.handValue.Total and myHandEval.handValue.Total > hand3Eval.handValue.Total:
                print('you win')
            elif hand1Eval.handValue.Total > myHandEval.handValue.Total and hand1Eval.handValue.Total > hand2Eval.handValue.Total and hand1Eval.handValue.Total > hand3Eval.handValue.Total:
                print('player 1 wins')
            elif hand2Eval.handValue.Total > myHandEval.handValue.Total and hand2Eval.handValue.Total > hand1Eval.handValue.Total and hand2Eval.handValue.Total > hand3Eval.handValue.Total:
                print('player 2 wins')
            elif hand3Eval.handValue.Total > myHandEval.handValue.Total and hand3Eval.handValue.Total > hand2Eval.handValue.Total and hand3Eval.handValue.Total > hand1Eval.handValue.Total:
                print('player 3 wins')
            elif myHandEval.handValue.HighCard > hand1Eval.handValue.HighCard and myHandEval.handValue.HighCard > hand2Eval.handValue.HighCard and myHandEval.handValue.HighCard > hand3Eval.handValue.HighCard:
                print('you win')
            elif hand1Eval.handValue.HighCard > myHandEval.handValue.HighCard and hand1Eval.handValue.HighCard > hand2Eval.handValue.HighCard and hand1Eval.handValue.HighCard > hand3Eval.handValue.HighCard:
                print('player 1 wins')
            elif hand2Eval.handValue.HighCard > myHandEval.handValue.HighCard and hand2Eval.handValue.HighCard > hand1Eval.handValue.HighCard and hand2Eval.handValue.HighCard > hand3Eval.handValue.HighCard:
                print('player 2 wins')
            elif hand3Eval.handValue.HighCard > myHandEval.handValue.HighCard and hand3Eval.handValue.HighCard > hand2Eval.handValue.HighCard and hand3Eval.handValue.HighCard > hand1Eval.handValue.HighCard:
                print('player 3 wins')


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
