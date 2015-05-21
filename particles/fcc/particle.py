from heppy_fcc.particles.particle import Particle as BaseParticle
from ROOT import TLorentzVector
import math

class Particle(BaseParticle):
    def __init__(self, fccptc):
        self.fccptc = fccptc
        self._charge = fccptc.read().Core.Charge
        self._pid = fccptc.read().Core.Type
        self._status = fccptc.read().Core.Status
        self._tlv = TLorentzVector()
        p4 = fccptc.read().Core.P4
        self._tlv.SetXYZM(p4.Px, p4.Py, p4.Pz, p4.Mass)
        
