import logging, threading
import os.path
from . import errhndl

class User():
    """A logged in user"""
    def __init__(self, socket):
        self.socket = socket
        self.thread = threading.Thread(target=self.loop)
    def loop(self):
        """Login user and start game"""
        self.socket.sendall("Username: ")
        self.username = self.socket.recv(2048).strip()
        if not os.path.isfile(os.path.join("users",self.username)):
            self.socket.sendall("You are not one of us\n")
            self.socket.close()
            return
        self.socket.sendall("Password: ")
        self.password = self.socket.recv(2048).strip()
        try:
            f = open(os.path.join("users", self.username))
            data = f.read().split('\n')
            #first line should contain password in base64 (white characters)"""
            if self.password.encode('base64').strip() != data[0]:
                raise Exception('wrong password')
        except:
            self.socket.sendall(errhndl.plea_for_advice())
            self.socket.sendall("Wrong username or password\n")
            self.socket.close()
            logging.info('Failed login attempt for user %s' % (self.username))
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
            if len(data) > 0:
                if data[0] in actions:
                    actions[data[0]](self, data[1:])
#               now check location related actions (like moving, since there will be many types of
#               movement, it will be better to hold it in Location class (like 'n', 'south', 'upstairs')
#               elif data[0] in self.location.actions:
#                   self.location.actions[data[0]](self.location, self, adata[1:])
                else:
                    self.socket.sendall(errhndl.plea_for_advice())
                    self.socket.sendall("Wrong action\n")
            else:
                self.socket.sendall(errhndl.plea_for_advice())
                self.socket.sendall("Say something, yo\n")
#           here put saving state to a file
    
    def say(self, arguments):
#       should be something like that, current is just for testing
#        for user in self.location.users:
#           user.socket.sendall('%s says: %s' % (self.username, " ".join(arguments)))
        self.socket.sendall('%s says: %s\n'%(self.username, ' '.join(arguments)))
    def cheat(self, arguments):
        self.socket.sendall("You attempt to cheat, but Almighty Nuclear Particles detect it and render you disconnected from the server.\n")
        self.quit(arguments)
    def quit(self, arguments):
        self.socket.close()
        logging.info('User %s disconnected' % self.username)
        self.connected = False

"""dict with all actions user can take in every situation (or almost :P)"""
actions={'say': User.say, 'quit': User.quit, 'cheat': User.cheat}
