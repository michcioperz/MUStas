import os, logging
from dunnohowtnameit.user import movement_full

class Map(object):
    """A map"""
    def __init__(self):
        self.locations = {}
    def load(self, directory):
        """load map from directory, each file in directory is a location"""
        for location in os.listdir(directory):
            try:
                l = Location()
                l.load(os.path.join(directory, location), location)
            except IOError:
                logging.error("Error during loading location %s/%s", directory, location)
            finally:
                self.locations[location] = l

class Location(object):
    """A location"""
    def __init__(self):
        self.description = ""
        self.users = set()
        self.movements = {}
        self.ident = None

    def load(self, filename, ident):
        """load location from file"""
        self.ident = ident
        f = open(filename, 'r')

        #load description, until a line containing only '-'
        while True:
            line = f.readline()
            if line.strip() == '-' or line == '':
                break
            self.description += line

        #load possible movements (and for now only this)
        while True:
            line = f.readline()
            if line == '':
                break
            if line.split()[0] == 'out':
                self.movements[line.split()[1]] = line.split()[2]

    def sendall(self,msg):
        """send msg to all users in this location"""
        for user in self.users:
            user.socket.sendall(msg)

    def desc(self, user, movements=True, users=True):
        """get more detailed description visible for an user"""
        desc = self.description
        if movements and len(self.movements) > 0:
            desc += 'You can go: %s\n'%', '.join(map(lambda i: movement_full[i], self.movements))
        if users and len(self.users) > 1:
            desc += 'You see here: %s\n'%', '.join([u.username for u in self.users if u != user])
        return desc

class Mob(object):
    """A mob"""
    pass
