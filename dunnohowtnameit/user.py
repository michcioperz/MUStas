import logging, threading

class User():
    """A logged in user"""
    def __init__(self, socket):
        self.socket = socket
        self.thread = threading.Thread(target=self.loop)
    def loop(self):
        """Login user and start game"""
        self.socket.sendall("Username: ")
        self.username = self.socket.recv(2048).strip()
        self.socket.sendall("Password: ")
        password = self.socket.recv(2048).strip()
        try:
            f = open("users/"+self.username)
            data = f.read().split('\n')
            """first line should password"""
            if password != data[0]:
                raise Exception('wrong password')
        except:
            self.socket.sendall("Wrong username or password\n")
            self.socket.close()
            logging.info('Failed loggin attempt')
            return
        logging.info('User %s logged in' % self.username)

        #here parse more data from data :P

        while True:
            data = self.socket.recv(2048)
            if len(data) == 0:
                logging.info('User %s disconnected' % self.username)
                return
            self.socket.sendall(data)
