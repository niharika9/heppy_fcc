from vectors import Point
from math import sqrt, sin
from ROOT import TVector2

class Info(object):
    pass

class Propagator(object):

    def propagate(self, particles, cylinders):
        for ptc in particles:
            for cyl in cylinders:
                self.propagate_one(ptc, cyl)
                
                
class StraightLinePropagator(Propagator):        

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

        
class HelixPropagator(object):
    
    def propagate_one(self, particle, cylinder, debug_info=None):
        field = 4. 
        rho = particle.p4.Perp() / (abs(particle.charge)*field)
        ## looking for helix center in xy plane
        # perp to momentum in xy plane:
        momperp_xy = TVector2(-particle.p4.Y(), particle.p4.X()).Unit()
        vertex_xy = TVector2(particle.vertex.X(), particle.vertex.Y())
        center_xy = vertex_xy - particle.charge * momperp_xy * rho
        print 'center',center_xy.X(), center_xy.Y()
        extreme_point_xy = TVector2(rho, 0) 
        if center_xy.X()!=0 or center_xy.Y()!=0:
            extreme_point_xy = center_xy + center_xy.Unit() * rho
        is_looper = extreme_point_xy.Mod() < cylinder.rad
        is_positive = particle.p4.Z() > 0.
        # destz = cylinder.z if positive else -cylinder.z
        info = Info()
        info.is_positive = is_positive
        info.is_looper = is_looper
        return info
        
straight_line = StraightLinePropagator()

helix = HelixPropagator() 
