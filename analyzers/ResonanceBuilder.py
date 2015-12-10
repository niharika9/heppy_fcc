from heppy.framework.analyzer import Analyzer
from heppy_fcc.particles.tlv.particle import Particle 

import pprint 
import itertools

mass = {23: 91, 25: 125}

class Resonance(Particle):
    def __init__(self, leg1, leg2, pdgid, status=3): 
        self.leg1 = leg1 
        self.leg2 = leg2 
        self._tlv = leg1.p4() + leg2.p4()
        self._charge = leg1.q() + leg2.q()
        self._pid = pdgid
        self._status = status

class ResonanceBuilder(Analyzer):
    
    def process(self, event):
        # legs = event.gen_particles_stable
        legs = getattr(event, self.cfg_ana.leg_collection)
        legs = [leg for leg in legs if self.cfg_ana.filter_func(leg)]
        resonances = []
        for leg1, leg2 in itertools.combinations(legs,2):
            resonances.append( Resonance(leg1, leg2, self.cfg_ana.pdgid, 3) )
        # sorting according to distance to nominal mass
        nominal_mass = mass[self.cfg_ana.pdgid]
        resonances.sort(key=lambda x: abs(x.m()-nominal_mass))
        setattr(event, self.instance_label, resonances)
        best = None
        if len(resonances):
            best = resonances[0]
        setattr(event, '_'.join([self.instance_label,'best']), best )
