from vectors import Point
from math import sqrt, sin

class StraightLinePropagator(object):        

    def propagate_one(self, particle, cylinder):
        udir = particle.p4.Vect().Unit()
        theta = udir.Theta()
        origin = particle.vertex
        if udir.Z():
            destz = cylinder.z if udir.Z() > 0. else -cylinder.z
            length = (destz - origin.Z())/udir.Z()
            assert(length>=0)
            destination = origin + udir * length
            rdest = destination.Perp()
            if rdest > cylinder.rad:
                length -= (rdest-cylinder.rad) / sin(theta)
                destination = origin + udir * length
        #TODO deal with Z == 0 
        #TODO deal with overlapping cylinders
        particle.points[cylinder.name] = destination

    def propagate(self, particles, cylinders):
        for ptc in particles:
            for cyl in cylinders:
                self.propagate_one(ptc, cyl)
        
class HelixPropagator(object):

    def propagate(self, particle, cylinder):
        pass
        
        
straight_line = StraightLinePropagator()

