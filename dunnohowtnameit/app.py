import logging, socket
from dunnohowtnameit.user import User, logged_in
from dunnohowtnameit.world import Map

def start(host='127.0.0.1', port=7999, loglevel=logging.INFO):
    m = Map()
    m.load('world')

    logging.basicConfig(level=loglevel)
    logging.info('Creating socket...')
    serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    serversocket.bind((host, port))
    serversocket.listen(5)
    logging.info('Now listening on %s:%i...' % (host, port,))
    while True:
        try:
            clientsocket, address = serversocket.accept()
            logging.debug('Accepting new client connection')
            clientsocket.settimeout(1)
            user = User(clientsocket, m)
            user.thread.start()
        except KeyboardInterrupt:
            logging.info('Closing server...')

            for user in logged_in.values():
                user.interrupt = True
            for user in logged_in.values():
                user.thread.join()
                user.socket.sendall('Closing server\n')
                user.close()
                user.socket.close()

            serversocket.close()
            logging.info('Server closed')
            return
