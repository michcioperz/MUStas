import logging, threading, os.path
from . import errhndl
from hashlib import sha512

DEFAULT_PROMPT = ">>> "
movement_short={'north':'n', 'south':'s', 'west':'w', 'east':'e', 'up':'u', 'down':'d'}
movement_full=dict(zip(movement_short.values(), movement_short.keys()))
movement_opposite={'north':'south', 'up':'down', 'east':'west'}
movement_opposite.update(dict(zip(movement_opposite.values(), movement_opposite.keys())))
movements=movement_full.keys()+movement_full.values()

class User():
    """A logged in user"""
    def __init__(self, socket, m):
        self.socket = socket
        self.thread = threading.Thread(target=self.loop)
        self.prompt = DEFAULT_PROMPT
        self.m = m
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
            #first line should contain sha512 hash of password
            if sha512(self.password + self.username).hexdigest() != data[0]:
                raise Exception('wrong password')
        except:
            self.socket.sendall(errhndl.plea_for_advice())
            self.socket.sendall("Wrong username or password\n")
            self.socket.close()
            logging.info('Failed login attempt for user %s' % (self.username))
            return
        logging.info('User %s logged in' % self.username)

        #here parse more data from data :P
        self.location = self.m.locations['1']
        self.location.sendall('%s appears from nowhere\n'%self.username)
        self.socket.sendall(self.location.desc())
        self.location.users.add(self)
        self.connected = True
        while self.connected:
            self.socket.sendall(self.prompt)
            data = self.socket.recv(2048)
            if len(data) == 0:
                self.socket.close()
                logging.info('User %s disconnected' % self.username)
                self.connected = False
                break
            data = data.strip().split()
            if len(data) > 0:
                if data[0] in actions:
                    actions[data[0]](self, data[1:])
#               now check location related actions (like moving, since there will be many types of
#               movement, it will be better to hold it in Location class (like 'n', 'south', 'upstairs')
                elif data[0] in movements:
                    self.moveto(data[0])
                else:
                    self.socket.sendall(errhndl.plea_for_advice())
                    self.socket.sendall("Wrong action\n")
            else:
                self.socket.sendall(errhndl.plea_for_advice())
                self.socket.sendall("Say something, yo\n")
        self.location.users.remove(self)
        self.location.sendall('%s disappears suddenly\n'%(self.username))
#           here put saving state to a file
    def moveto(self, movement):
        if movement in movement_short.keys():
            movement = movement_short[movement]
        full = movement_full[movement]
        if movement in self.location.movements.keys():
            destination = self.location.movements[movement]
            self.location.users.remove(self)
            self.location.sendall('%s goes %s\n'%(self.username, full))
            self.socket.sendall('you go %s\n'%full)
            self.location = self.m.locations[destination]
            self.location.sendall('%s comes from %s\n'%(self.username, movement_opposite[full]))
            self.socket.sendall(self.location.desc())
            self.location.users.add(self)
        else:
            self.socket.sendall("you can't go %s\n"%movement_full[movement])

    def say(self, arguments):
        self.location.sendall('%s says: %s\n'%(self.username, ' '.join(arguments)))
    def cheat(self, arguments):
        self.socket.sendall("You attempt to cheat, but Almighty Nuclear Particles detect it and render you disconnected from the server.\n")
        self.quit(arguments)
    def quit(self, arguments):
        self.socket.close()
        logging.info('User %s disconnected' % self.username)
        self.connected = False

"""dict with all actions user can take in every situation (or almost :P)"""
actions={'say': User.say, 'quit': User.quit, ':q': User.quit, ':wq': User.quit, ':q!': User.quit, 'exit': User.quit, 'leave': User.quit, 'cheat': User.cheat, 'hack': User.cheat}
