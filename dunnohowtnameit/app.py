import logging, socket
from user import User
from world import World

def start(host='127.0.0.1', port=7999, loglevel=logging.INFO):
    logging.basicConfig(level=loglevel)
    logging.info('Creating socket...')
    serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serversocket.bind((host, port))
    serversocket.listen(5)
    logging.info('Now listening on %s:%i...' % (host, port,))
    while True:
        clientsocket, address = serversocket.accept()
        logging.debug('Accepting new client connection')
        user = User(clientsocket)
        user.thread.start()
