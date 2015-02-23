from vectors import Point
from collections import OrderedDict


class Cluster(object):

    max_energy = 0.
    
    def __init__(self, energy, position, size, layer, particle=None):
        self.energy = energy
        if self.energy > self.__class__.max_energy:
            self.__class__.max_energy = self.energy
        self.position = position
        self.size = size
        self.layer = layer
        self.particle = particle

        
class Trajectory(object):
    def __init__(self, p3, vertex):
        self.p3 = p3
        self.points = OrderedDict()
        self.points['vertex'] = vertex

        
class Particle(Trajectory):
    def __init__(self, p4, vertex, charge, pdgid=None):
        self.p4 = p4
        self.vertex = vertex
        self.charge = charge
        self.pdgid = pdgid
        self.helix = None
        self.clusters = dict()
        super(Particle, self).__init__(p4.Vect(), vertex)

    def is_em(self):
        kind = abs(self.pdgid)
        if kind==11 or kind==22:
            return True
        else:
            return False
        
    def set_helix(self, helix):
        self.helix = helix
        
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
    
