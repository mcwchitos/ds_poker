from flask import Flask, request, make_response
from Card import DealCards
import requests
from collections import deque

app = Flask(__name__)
ips = []
order = False
dc = DealCards()


@app.route('/getcards')
def getCards():
    return 'hi'


@app.route('/register')
def register():
    response = requests.get('http://127.0.0.1:5000/register')
    if response.status_code == 400:
        return make_response('failed', 400)

    elif response.status_code == 200:
        return make_response('succeed', 200)


@app.route('/connect', methods=['POST'])
def connection():
    global ips, order

    json = request.get_json()
    ips.append(json['ip1'])
    ips.append(json['ip2'])
    ips.append(json['ip3'])
    ips.append(json['ip4'])
    ips = deque(ips)
    my = 'http://' + request.host + '/'
    if my == ips[0]:
        order = True
        start()
    ips.rotate(-ips.index(my))

    return make_response('succeed', 200)


@app.route('/start', methods=['POST'])
def start():
    global ips
    dc.Deal()
    my = 'http://' + request.host + '/'
    dc.DisplayMyCards(ips.index(my))
    print('-------------------------')
    dc.DisplayCards()
    return 'hi'


@app.route('/update')
def update():
    return 'hi'


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5544, debug=True)

# dc = DealCards()
# dc.Deal()
# dc.DisplayCards()
