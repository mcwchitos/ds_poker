# from Card import *
#
# dc = DealCards()
# dc.Deal()
# dc.DisplayMyCards(0)
#
# for i in range(2):
#     print('want to change the card? (Y-N)')
#     ans = input()
#     if ans == 'Y':
#         dc.getCard(0, int(input()))
#         dc.DisplayMyCards(0)
# dc.evaluateHands()
# dc.DisplayCards()

n = 1

list_1 = [1, 2, 3, 4]
list_1 = (list_1 [n : len(list_1)]+ list_1[0:n])
print(list_1)