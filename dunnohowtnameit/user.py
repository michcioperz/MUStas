import logging, threading, os.path
from . import errhndl
from hashlib import sha512

DEFAULT_PROMPT = ">>> "
#possible movements and some usefull dicts
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
        self.location = None
        self.line = ''

    def loop(self):
        """Login user and start the game"""
        self.socket.sendall("Username: ")
        try:
            self.username = self.getline()
        except:
            return
        if not os.path.isfile(os.path.join("users",self.username)):
            self.socket.sendall("You are not one of us\n")
            self.socket.close()
            return
        self.socket.sendall("Password: ")
        try:
            self.password = self.getline()
        except:
            return
        try:
            f = open(os.path.join("users", self.username))
            data = f.read().split('\n')
            if sha512(self.password + self.username).hexdigest() != data[0]:
                raise Exception('wrong password')
        except:
            self.socket.sendall(errhndl.plea_for_advice())
            self.socket.sendall("Wrong username or password\n")
            self.socket.close()
            logging.info('Failed login attempt for user %s' % (self.username))
            return
        if self.username not in logged_in.keys():
            logged_in[self.username] = self
        else:
            self.socket.sendall("You are already logged in\n");
            self.socket.close()
            return

        logging.info('User %s logged in' % self.username)

        #move user to starting location, 1 for now
        self.moveto('1', 'nowhere')

        self.connected = True
        while self.connected:
            self.socket.sendall(self.prompt)
            try:
                data = self.getline()
            except:
                logging.info('User %s disconnected' % self.username)
                self.connected = False
                break

            data = data.strip().split()
            if len(data) > 0:
                if data[0] in actions:
                    actions[data[0]](self, data[1:])
                elif data[0] in movements:
                    self.move(data[0])
                else:
                    self.socket.sendall(errhndl.plea_for_advice())
                    self.socket.sendall("Wrong action\n")
            else:
                self.socket.sendall(errhndl.plea_for_advice())
                self.socket.sendall("Say something, yo\n")

        self.location.users.remove(self)
        self.location.sendall('%s disappears suddenly\n'%(self.username))
        del logged_in[self.username]

    def move(self, movement):
        """move user in a specyfied direction"""
        if movement in movement_short.keys():
            movement = movement_short[movement]
        full = movement_full[movement]
        if movement in self.location.movements.keys():
            destination = self.location.movements[movement]
            self.moveto(destination, movement_opposite[full], full)
        else:
            self.socket.sendall("you can't go %s\n"%movement_full[movement])

    def moveto(self, destination, comesfrom, full=""):
        """move to specified destination"""
        if self.location is not None:
            self.location.users.remove(self)
            self.location.sendall('%s goes %s\n'%(self.username, full))
            self.socket.sendall('you go %s\n'%full)
        self.location = self.m.locations[destination]
        self.location.sendall('%s comes from %s\n'%(self.username, comesfrom))
        self.socket.sendall(self.location.desc())
        self.location.users.add(self)

    def say(self, arguments):
        self.location.sendall('%s says: %s\n'%(self.username, ' '.join(arguments)))

    def cheat(self, arguments):
        self.socket.sendall("You attempt to cheat, but Almighty Nuclear Particles detect\
                it and render you disconnected from the server.\n")
        self.quit(arguments)

    def quit(self, arguments):
        self.socket.close()
        logging.info('User %s disconnected' % self.username)
        self.connected = False

    def getline(self):
        while '\n' not in self.line:
            new = self.socket.recv(2048)
            if len(new) == 0:
                self.socket.close()
                raise "Connection end"
            self.line += new.replace('\r', '')
        ls = self.line[:self.line.find('\n')]
        self.line = self.line[self.line.find('\n')+1:]
        return ls

"""dict with all actions user can take in every situation (or almost :P)"""
actions={'say': User.say, 'quit': User.quit, ':q': User.quit, ':wq': User.quit, ':q!': User.quit, 'exit': User.quit, 'leave': User.quit, 'cheat': User.cheat, 'hack': User.cheat}

"""dict with all logged in users"""
logged_in={}
