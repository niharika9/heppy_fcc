from vectors import Point
import math
import copy
from ROOT import TVector3
from geotools import circle_intersection
from heppy.utils.deltar import deltaPhi
from helix import Helix

class Info(object):
    pass

class Propagator(object):

    def propagate(self, particles, *args, **kwargs):
        for ptc in particles:
            for cyl in cylinders:
                self.propagate_one(ptc, *args, **kwargs)
                
                
class StraightLinePropagator(Propagator):        

    def propagate_one(self, particle, cylinder, dummy=None):
        udir = particle.p4.Vect().Unit()
        theta = udir.Theta()
        origin = particle.vertex
        if udir.Z():
            destz = cylinder.z if udir.Z() > 0. else -cylinder.z
            length = (destz - origin.Z())/math.cos(theta)
            # import pdb; pdb.set_trace()
            assert(length>=0)
            destination = origin + udir * length
            rdest = destination.Perp()
            if rdest > cylinder.rad:
                udirxy = TVector3(udir.X(), udir.Y(), 0.)
                originxy = TVector3(origin.X(), origin.Y(), 0.)
                # solve 2nd degree equation for intersection
                # between the straight line and the cylinder
                # in the xy plane to get k,
                # the propagation length
                a = udirxy.Mag2()
                b= 2*udirxy.Dot(originxy)
                c= originxy.Mag2()-cylinder.rad**2
                delta = b**2 - 4*a*c
                km = (-b - math.sqrt(delta))/(2*a)
                # positive propagation -> correct solution.
                kp = (-b + math.sqrt(delta))/(2*a)
                # print delta, km, kp
                destination = origin + udir * kp  
        #TODO deal with Z == 0 
        #TODO deal with overlapping cylinders
        particle.points[cylinder.name] = destination

        
class HelixPropagator(Propagator):
    
    def propagate_one(self, particle, cylinder, field, debug_info=None):
        helix = Helix(field, particle.charge, particle.p4,
                      particle.vertex)
        particle.set_helix(helix)
        is_looper = helix.extreme_point_xy.Mag() < cylinder.rad
        is_positive = particle.p4.Z() > 0.
        if not is_looper:
            xm, ym, xp, yp = circle_intersection(helix.center_xy.X(),
                                                 helix.center_xy.Y(),
                                                 helix.rho,
                                                 cylinder.rad)
            # particle.points[cylinder.name+'_m'] = Point(xm,ym,0)
            # particle.points[cylinder.name+'_p'] = Point(xp,yp,0)
            phi_m = helix.phi(xm, ym)
            phi_p = helix.phi(xp, yp)
            dest_time = helix.time_at_phi(phi_p)
            destination = helix.point_at_time(dest_time)
            if destination.Z()*helix.udir.Z()<0.:
                dest_time = helix.time_at_phi(phi_m)
                destination = helix.point_at_time(dest_time)
            if abs(destination.Z())<cylinder.z:
                particle.points[cylinder.name] = destination
            else:
                is_looper = True
        if is_looper:
            # extrapolating to endcap
            destz = cylinder.z if helix.udir.Z() > 0. else -cylinder.z
            dest_time = helix.time_at_z(destz)
            destination = helix.point_at_time(dest_time)
            # destz = cylinder.z if positive else -cylinder.z
            particle.points[cylinder.name] = destination

            
        info = Info()
        info.is_positive = is_positive
        info.is_looper = is_looper
        return info
        
straight_line = StraightLinePropagator()

helix = HelixPropagator() 
