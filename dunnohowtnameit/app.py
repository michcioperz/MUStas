import socket
from user import User
from world import World

def start(host='127.0.0.1', port=7999):
    print 'creating socket...'
    serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serversocket.bind((host, port))
    serversocket.listen(5)
    print 'listening...'
    while True:
        clientsocket, address = serversocket.accept()
        print 'new client connected'
        user = User(clientsocket)
        user.thread.start()
