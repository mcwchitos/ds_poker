import threading

from flask import Flask, request, make_response, json, jsonify
from Card import DealCards, Card
from flask_cors import CORS, cross_origin
from celery import *
import requests

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
ips = []
my = 'http://'
turn = False
isEnd = False
dc = DealCards()
dc.Deal()

@app.route('/evaluateHands')
def checkHands():
    global ips, dc, my
    result = dc.evaluateHands
    isWinner =  result - 1 == ips.index(my)
    if isWinner:
        dc.playerCoins[ips.index(my)] += dc.bank
        for i in range(len(dc.bets)):
            dc.bets[i] = 0
        dc.bank = 0
    return json.jsonify({'isWinned': isWinner, 'newAmount': dc.playerCoins[ips.index(my)]})

@app.route('/getCards')
def getCards():
    global ips, dc, my
    cards = dc.getCards(ips.index(my))
    result = []
    for card in cards:
        result.append({'suit': card.SUIT, 'value': card.VALUE})

    return json.jsonify(result)


@app.route('/bank', methods=['GET'])
def getBank():
    global dc
    return json.jsonify(dc.bank)


@app.route('/changeCards', methods=['GET'])
@cross_origin()
def changeCards():
    global dc, my
    index = request.args.get('index')
    arr = index[1:-1].split(',')
    for ind in arr:
        dc.getCard(ips.index(my), int(ind))

    cards = dc.getCards(ips.index(my))
    result = []
    for card in cards:
        result.append({'suit': card.SUIT, 'value': card.VALUE})
    response = json.jsonify(result)
    return response

@app.route('/getIsTurn', methods=['GET'])
def getIsTurn():
    global turn
    return json.jsonify(turn)


@app.route('/connect', methods=['POST'])
@cross_origin()
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

@app.route('/updateAmount', methods=['GET'])
@cross_origin()
def updateAmount():
    global dc, ips, my, turn, isEnd
    amount = request.args.get('amount')
    dc.bet(ips.index(my), int(amount))
    print(dc.playerCoins)
    if dc.bets[0] == dc.bets[1] and dc.bets[0] == dc.bets[2] and dc.bets[0] == dc.bets[3] and dc.bets[0] != 0:
        turn = False
        isEnd = True
    updateAll()
    return json.jsonify({'amounts': dc.playerCoins, 'isEnd': isEnd})



@app.route('/getAmounts', methods=['GET'])
def getAmounts():
    global dc
    return json.jsonify(dc.playerCoins)

@app.route('/getBets', methods=['GET'])
def getBets():
    global dc
    return json.jsonify(dc.bets)


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
@cross_origin()
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
    print(turn)
    display()
    return 'hi'

PORT = 5544
@app.route('/')
def index():
    url = 'http://127.0.0.1:5000/register'
    requests.get(url, json=str(PORT))
    return 'ok'


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=PORT, debug=True)

