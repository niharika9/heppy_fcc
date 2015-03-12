import random
from vectors import * 
import math

from pfobjects import Particle

m_e = 0.000511
m_mu = 0.105
m_pi = 0.139
m_pi0 = 0.145
m_n = 1.
m_p = 1. 
particle_data = {
    11 : (m_e, 1),    
    -11 : (m_e, -1),    
    13 : (m_mu, 1),    
    -13 : (m_mu, -1),    
    22 : (0., 0),
    130 : (m_pi0, 0),
    211 : (m_pi, 1),
    -211 : (m_pi, -1)
    }

def particles(nptcs, pdgid, thetamin, thetamax, emin, emax, vertex=None ):
    ngenerated = 0
    mass, charge = particle_data[pdgid]
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
        yield Particle(p4, vertex, charge, pdgid) 

        
def monojet(pdgids, theta, jetmass, jetenergy):
    for pdgid in pdgids: 
        phistar = random.uniform(-math.pi, math.pi)
        thetastar = random.uniform(-math.pi, math.pi)
        
        
if __name__ == '__main__':
    for ptc in particles(10, 0., 0., 0.1, 0.2, 10, 50):
        print ptc
