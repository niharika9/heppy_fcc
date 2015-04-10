from heppy_fcc.particles.particle import Particle as BaseParticle
from ROOT import TLorentzVector
import math

class Particle(BaseParticle):
    def __init__(self, fccptc):
        self.fccptc = fccptc
        self.charge = fccptc.read().Core.Charge
        self.pid = fccptc.read().Core.Type        
        self.tlv = TLorentzVector()
        p4 = fccptc.read().Core.P4
        self.tlv.SetPtEtaPhiM(p4.Pt, p4.Eta, p4.Phi, p4.Mass)

