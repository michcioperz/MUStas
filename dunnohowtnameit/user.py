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
        self.password = self.socket.recv(2048).strip()
        try:
            f = open("users/"+self.username)
            data = f.read().split('\n')
            """first line should self.password"""
            if self.password != data[0]:
                raise Exception('wrong self.password')
        except:
            self.socket.sendall("Wrong username or self.password\n")
            self.socket.close()
            logging.info('Failed loggin attempt')
            return
        logging.info('User %s logged in' % self.username)

        #here parse more data from data :P
        self.connected = True
        while self.connected:
            data = self.socket.recv(2048)
            if len(data) == 0:
                self.socket.close()
                logging.info('User %s disconnected' % self.username)
                self.connected = False
            data = data.strip().split()
            if data[0] in actions:
                actions[data[0]](self, data[1:])
#           now check special location actions
#           elif data[0] in self.location.actions:
#               self.location.actions[data[0]](self.location, self, adata[1:])
            else:
                self.socket.sendall("Wrong action\n")
#       here put saving state to a file
    
    def say(self, arguments):
#       should be something like that, current is just for testing
#        for user in self.location.users:
#           user.socket.sendall('%s says: %s' % (self.username, " ".join(arguments)))
        self.socket.sendall('%s says: %s\n'%(self.username, ' '.join(arguments)))
    def quit(self, arguments):
        self.socket.close()
        logging.info('User %s disconnected' % self.username)
        self.connected = False

"""dict with all actions user can take in every situation (or almost :P)"""
actions={'say': User.say, 'quit' : User.quit}
