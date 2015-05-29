from heppy_fcc.particles.particle import Particle as BaseParticle
from ROOT import TLorentzVector
import math

class Particle(BaseParticle):
    
    def __init__(self, fccptc):
        self.fccptc = fccptc
        self._charge = fccptc.read().Core.Charge
        self._pid = fccptc.read().Core.Type
        self._status = fccptc.read().Core.Status
        start = fccptc.read().StartVertex
        self._start_vertex = start.read() if start.isAvailable() else None 
        end = fccptc.read().EndVertex
        self._end_vertex = end.read() if end.isAvailable() else None 
        self._tlv = TLorentzVector()
        p4 = fccptc.read().Core.P4
        self._tlv.SetXYZM(p4.Px, p4.Py, p4.Pz, p4.Mass)
        
