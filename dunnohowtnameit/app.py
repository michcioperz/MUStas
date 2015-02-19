import logging, socket
from dunnohowtnameit.user import User
from dunnohowtnameit.world import Map

def start(host='127.0.0.1', port=7999, loglevel=logging.INFO):
    m = Map()
    m.load('world')

    logging.basicConfig(level=loglevel)
    logging.info('Creating socket...')
    serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serversocket.bind((host, port))
    serversocket.listen(5)
    logging.info('Now listening on %s:%i...' % (host, port,))
    while True:
        try:
            clientsocket, address = serversocket.accept()
            logging.debug('Accepting new client connection')
            user = User(clientsocket, m)
            user.thread.start()
        except KeyboardInterrupt:
            logging.info('Closing server...')
            serversocket.close()
            return
