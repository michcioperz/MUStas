import logging, threading


class User():
    """A logged in user"""
    def __init__(self, socket):
        self.socket = socket
        self.thread = threading.Thread(target=self.loop)
    def loop(self):
        """Login user and start game"""
        self.socket.sendall("Hello\n")
        while True:
            data = self.socket.recv(2048)
            if len(data) == 0:
                logging.debug('Client disconnected')
                return
            self.socket.sendall(data)
