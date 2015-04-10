from heppy.framework.analyzer import Analyzer
from heppy_fcc.particles.fcc.particle import Particle 

import math
from heppy_fcc.fastsim.detectors.CMS import CMS
from heppy_fcc.fastsim.simulator import Simulator
from heppy_fcc.fastsim.vectors import Point
from heppy_fcc.fastsim.pfobjects import Particle as PFSimParticle
from heppy_fcc.fastsim.toyevents import particles
from heppy_fcc.display.core import Display
from heppy_fcc.display.geometry import GDetector
from heppy_fcc.display.pfobjects import GTrajectories

from ROOT import TLorentzVector, TVector3

def pfsimparticle(ptc):
    tp4 = ptc.p4()
    vertex = TVector3()
    charge = ptc.q()
    pid = ptc.pdgid()
    return PFSimParticle(tp4, vertex, charge, pid) 
        
class PFSim(Analyzer):

    def __init__(self, *args, **kwargs):
        super(PFSim, self).__init__(*args, **kwargs)
        self.detector = CMS()
        self.simulator = Simulator(self.detector, self.mainLogger)
        self.is_display = self.cfg_ana.display
        if self.is_display:
            self.init_display()        
        
    def init_display(self):
        self.display = Display(['xy','yz', 'ECAL_thetaphi', 'HCAL_thetaphi'])
        self.gdetector = GDetector(self.detector)
        self.display.register(self.gdetector, layer=0, clearable=False)
        self.is_display = True
        
    def process(self, event):
        # move the following to a gen particle analyzer at some point 
        if self.is_display:
            self.display.clear()
        store = event.input
        edm_particles = store.get("GenParticle")
        gen_particles_stable = []
        pfsim_particles = []
        for ptc in edm_particles:
            pyptc = Particle(ptc)
            core = ptc.read().Core
            if core.Status == 1 and core.P4.Pt>1.:
                gen_particles_stable.append( pyptc )
                pfsimptc = pfsimparticle(pyptc)
                pfsim_particles.append(pfsimptc)
                if self.cfg_ana.verbose:
                    print pyptc
        if self.cfg_ana.verbose:
            print 'stable/all particles = {s}/{a}'.format(s=len(gen_particles_stable),
                                                          a=len(edm_particles))
        self.simulator.simulate( pfsim_particles )
        if self.is_display:
            self.display.register( GTrajectories(pfsim_particles), layer=1)
        
        event.genparticles = gen_particles_stable
        event.simparticles = pfsim_particles
        event.particles = self.simulator.pfsequence.pfreco.particles 

