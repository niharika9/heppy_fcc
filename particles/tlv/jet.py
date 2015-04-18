from heppy_fcc.particles.jet import Jet as BaseJet

import math

class Jet(BaseJet):
    def __init__(self, tlv):
        self.tlv = tlv
