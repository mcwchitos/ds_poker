from flask import Flask, request, make_response, json
from Card import DealCards, Card
import requests

app = Flask(__name__)
ips = []
my = 'http://'
turn = False
dc = DealCards()
dc.Deal()


@app.route('/getcards')
def getCards():
    global ips, dc, my
    cards = dc.getCards(ips.index(my))
    result = []
    for card in cards:
        result.append({'suit': card.SUIT, 'value': card.VALUE})

    return json.jsonify(result)


@app.route('/register')
def register():
    response = requests.get('http://127.0.0.1:5000/register')
    if response.status_code == 400:
        return make_response('failed', 400)

    elif response.status_code == 200:
        return make_response('succeed', 200)


@app.route('/bank', methods=['GET'])
def getBank():
    global dc
    return json.jsonify(dc.bank)


@app.route('/changeCards', methods=['GET'])
def changeCards():
    global dc, my
    indexesToChange = request.args.getlist('indexesToChange')
    for index in indexesToChange:
        dc.getCard(ips.index(my), index)
    cards = dc.getCards(ips.index(my))
    result = []
    for card in cards:
        result.append({'suit': card.SUIT, 'value': card.VALUE})

    return json.jsonify(result)


@app.route('/isTurn', methods=['GET'])
def getIsTurn():
    global turn
    return json.jsonify(turn)


@app.route('/connect', methods=['POST'])
def connection():
    global ips, turn, my
    json = request.get_json()
    ips.append(json['ip1'])
    ips.append(json['ip2'])
    ips.append(json['ip3'])
    ips.append(json['ip4'])

    my = my + request.host + '/'
    print(my)
    if my == ips[0]:
        turn = True
        display()
    elif my == ips[1]:
        ips = (ips[1: len(ips)] + ips[0:1])
    elif my == ips[2]:
        ips = (ips[2: len(ips)] + ips[0:2])
    elif my == ips[3]:
        ips = (ips[3: len(ips)] + ips[0:3])
    print(ips)

    return make_response('succeed', 200)


@app.route('/start')
def start():
    updateAll()
    return 'ok'

@app.route('/updateAmount', methods=['POST'])
def updateAmount():
    global dc, ips, my
    amount = request.args.get('amount')
    dc.playerCoins[ips.index(my)] -= int(amount)
    print(dc.playerCoins)
    updateAll()
    return json.jsonify(dc.playerCoins)


@app.route('/getAmounts', methods=['GET'])
def getAmounts():
    global dc
    return json.jsonify(dc.playerCoins)


def display():
    global ips, dc, my
    dc.DisplayMyCards(ips.index(my))
    dc.DisplayCards()

    return 'hi'


def updateAll():
    global dc, ips, my, turn
    deck = dc.deck
    result = []
    for card in deck:
        result.append({'suit': card.SUIT, 'value': card.VALUE})
    players = []
    for hands in dc.playersHands:
        hand = []
        for card in hands:
            hand.append({'suit': card.SUIT, 'value': card.VALUE})
        players.append(hand)
    i = 1
    for ip in ips:
        if ip == my:
            continue
        data = {'ip': ips[1],
                'deck': result,
                'playerCoins': dc.playerCoins,
                'bets': dc.bets,
                'bank': dc.bank,
                'order': dc.order,
                'players': players,
                'rotate': i}
        url = ip + 'update'
        response = requests.post(url, json=data)
        print(response.status_code)
        turn = False
        i += 1
    return


@app.route('/update', methods=['POST'])
def update():
    global dc, turn, my
    json = request.get_json()

    ip = json['ip']
    deck = json['deck']
    playerCoins = json['playerCoins']
    bets = json['bets']
    bank = json['bank']
    order = json['order']
    players = json['players']
    rotate = json['rotate']

    hands = []
    for player in players:
        hand = []
        for card in player:
            hand.append(Card(card.get('suit'), card.get('value')))
        hands.append(hand)
    dc.playersHands = hands

    for i in range(len(dc.deck)):
        dc.deck[i] = Card(deck[i].get('suit'), deck[i].get('value'))
    dc.playerCoins = playerCoins
    dc.bets = bets
    dc.bank = bank
    dc.order = order

    if my == ip:
        turn = True
    dc.BetsRotate(rotate)
    dc.HandsRotate(rotate)
    dc.CoinsRotate(rotate)

    display()

    return 'hi'


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5533, debug=True)

