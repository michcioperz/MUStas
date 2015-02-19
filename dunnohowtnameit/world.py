import os, logging
from dunnohowtnameit.user import movement_short, movement_full

class Map():
    """A map"""
    def __init__(self):
        self.locations = {}
    def load(self,directory):
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
        self.id = id
        f = open(filename,'r')
        while True:
            line = f.readline()
            if line.strip() == '-' or line == '':
                break
            self.description += line
        while True:
            line = f.readline()
            if line == '':
                break
            if line.split()[0] == 'out':
                self.movements[line.split()[1]] = line.split()[2]
    def sendall(self,msg):
        for user in self.users:
            user.socket.sendall(msg)
    def desc(self):
        return (self.description + 'You can go: %s\nYou see here: %s\n'%(
                ', '.join(map(lambda i: movement_full[i], self.movements)),
                ', '.join([u.username for u in self.users])))



class Mob():
    """A mob"""
    pass
