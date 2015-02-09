from vectors import Point

class Cluster(object):
    def __init(self, energy, position, layer):
        self.energy = energy
        self.position = position
        self.layer = layer

        
class Trajectory(object):
    def __init__(self, p3, vertex):
        self.p3 = p3
        self.points = dict(
            vertex = vertex
        )
    
class Particle(Trajectory):
    def __init__(self, p4, vertex, charge):
        self.p4 = p4
        self.vertex = vertex
        self.charge = charge
        super(Particle, self).__init__(p4.Vect(), vertex)

class Track(Trajectory):
    pass
