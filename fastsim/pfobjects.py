from vectors import Point
from collections import OrderedDict

class Cluster(object):
    def __init(self, energy, position, layer):
        self.energy = energy
        self.position = position
        self.layer = layer

        
class Trajectory(object):
    def __init__(self, p3, vertex):
        self.p3 = p3
        self.points = OrderedDict()
        self.points['vertex'] = vertex
    
class Particle(Trajectory):
    def __init__(self, p4, vertex, charge):
        self.p4 = p4
        self.vertex = vertex
        self.charge = charge
        super(Particle, self).__init__(p4.Vect(), vertex)
        
    def __str__(self):
        return '{classname}: {charge} {mass:5.2f} {energy:5.2f} {theta:5.2f} {phi:5.2f}'.format(
            classname = self.__class__.__name__,
            charge = self.charge,
            mass = abs(self.p4.M()),
            energy = self.p4.E(),
            theta = self.p4.Theta(),
            phi = self.p4.Phi()
        )
        
class Track(Trajectory):
    pass
