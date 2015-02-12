import random
from vectors import * 
import math

from pfobjects import Particle

def particles(nptcs, charge, mass, thetamin, thetamax, emin, emax, vertex=None ):
    ngenerated = 0
    while ngenerated<nptcs: 
        theta = random.uniform(thetamin, thetamax)
        phi = random.uniform(-math.pi, math.pi)
        energy = random.uniform(emin, emax)
        if vertex is None:
            vertex = Point(0, 0, 0)
        momentum = math.sqrt(energy**2 - mass**2)
        costheta = math.cos(theta)
        sintheta = math.sin(theta)
        cosphi = math.cos(phi)
        sinphi = math.sin(phi)        
        p4 = LorentzVector(momentum*sintheta*cosphi,
                           momentum*sintheta*sinphi,
                           momentum*costheta,
                           energy)
        ngenerated += 1
        yield Particle(p4, vertex, charge) 


        
if __name__ == '__main__':
    for ptc in particles(10, 0., 0., 0.1, 0.2, 10, 50):
        print ptc
