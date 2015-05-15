from heppy.framework.analyzer import Analyzer
from heppy_fcc.fastsim.pdt import particle_data
from heppy_fcc.particles.tlv.particle import Particle 

import math
import random

from ROOT import TLorentzVector

def particle(pdgid, theta, phi, energy):
    mass, charge = particle_data[pdgid]
    momentum = math.sqrt(energy**2 - mass**2)
    costheta = math.cos(math.pi/2. - theta)
    sintheta = math.sin(math.pi/2. - theta)
    cosphi = math.cos(phi)
    sinphi = math.sin(phi)        
    tlv = TLorentzVector(momentum*sintheta*cosphi,
                         momentum*sintheta*sinphi,
                         momentum*costheta,
                         energy)
    return Particle(pdgid, charge, tlv) 
    

class Gun(Analyzer):
    
    def process(self, event):
        theta = random.uniform(-math.pi, math.pi)
        energy = random.uniform(1., 50)
        event.gen_particles = [particle(211, theta, 0., energy)]
        event.gen_particles_stable = event.gen_particles
