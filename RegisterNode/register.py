from flask import Flask, request, make_response
import requests

app = Flask(__name__)

numOfPlayers = 0
ips = []


@app.route('/')
def hi():
    print(str(request.environ.get('REMOTE_PORT')))
    return 'hi'

@app.route('/disconnect')
def disconnect():
    return 'hi'

@app.route('/register')
def register():
    global ips, numOfPlayers
    port = request.json
    new_ip = 'http://' + request.remote_addr + ':' + str(port) + '/'
    print(new_ip, ips)
    if new_ip in ips:
        return make_response('already', 200)
    if numOfPlayers > 4:
        return make_response('error', 400)
    else:
        print(new_ip, numOfPlayers)
        ips.append(new_ip)
        numOfPlayers += 1
    if numOfPlayers == 4:
        connect()
    print(numOfPlayers)
    return make_response('success', 200)


@app.route('/connect')
def connect():
    global ips
    for ip in ips:
        data = {'ip1': ips[0], 'ip2': ips[1], 'ip3': ips[2], 'ip4': ips[3]}
        url = ip + 'connect'
        response = requests.post(url, json=data)
        print(response.status_code)

    url = ips[0] + 'start'
    response = requests.get(url)
    print(response.status_code)
    return 'hi'


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)
