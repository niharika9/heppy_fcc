from heppy_fcc.particles.particle import Particle as BaseParticle

import math

class Particle(BaseParticle):
    def __init__(self, pdgid, charge, tlv):
        self.pid = pdgid
        self.charge = charge
        self.tlv = tlv
