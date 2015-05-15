from heppy.framework.analyzer import Analyzer
from heppy_fcc.fastsim.pdt import particle_data
from heppy_fcc.particles.tlv.particle import Particle 

import math
import random

from ROOT import TLorentzVector

def particle(pdgid, theta, phi, energy, flat_pt=False):
    mass, charge = particle_data[pdgid]
    costheta = math.cos(math.pi/2. - theta)
    sintheta = math.sin(math.pi/2. - theta)
    tantheta = sintheta / costheta
    cosphi = math.cos(phi)
    sinphi = math.sin(phi)        
    if do_pt:
        pt = energy
        momentum = pt / sintheta
        energy = math.sqrt(momentum**2 + mass**2)
    else:
        momentum = math.sqrt(energy**2 - mass**2)
    tlv = TLorentzVector(momentum*sintheta*cosphi,
                         momentum*sintheta*sinphi,
                         momentum*costheta,
                         energy)
    return Particle(pdgid, charge, tlv) 
    

class Gun(Analyzer):
    
    def process(self, event):
        theta = random.uniform(-math.pi+0.1, math.pi-0.1)
        energy = random.uniform(0.1, 50)
        event.gen_particles = [particle(211, theta, 0., energy, flat_pt=True)]
        event.gen_particles_stable = event.gen_particles
