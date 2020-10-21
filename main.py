from Card import *

dc = DealCards()
dc.Deal()
dc.DisplayMyCards()

for i in range(2):
    print('want to change the card? (Y-N)')
    ans = input()
    if ans == 'Y':
        dc.getCard(int(input()))
        dc.DisplayMyCards()
dc.evaluateHands()
dc.DisplayCards()
