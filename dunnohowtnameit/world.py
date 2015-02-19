import os, logging
from dunnohowtnameit.user import movement_short, movement_full

class Map():
    """A map"""
    def __init__(self):
        self.locations = {}
    def load(self,directory):
        """load map from directory, each file in directory is a location"""
        for location in os.listdir(directory):
            try:
                l = Location()
                l.load(os.path.join(directory, location), location)
            except:
                logging.error("Error during loading location %s/%s"%(directory, location))
            finally:
                self.locations[location] = l

class Location():
    """A location"""
    def __init__(self):
        self.description=""
        self.users=set()
        self.movements={}
        self.id = None

    def load(self,filename, id):
        """load location from file"""
        self.id = id
        f = open(filename,'r')

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

    def desc(self, movements=True, users=True):
        """get more detailed description"""
        desc = self.description
        if movements and len(self.movements) > 0:
            desc += 'You can go: %s\n'%', '.join(map(lambda i: movement_full[i], self.movements))
        if users and len(self.users) > 0:
            desc += 'You see here: %s\n'%', '.join([u.username for u in self.users])
        return desc

class Mob():
    """A mob"""
    pass
