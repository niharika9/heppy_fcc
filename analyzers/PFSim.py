from heppy.framework.analyzer import Analyzer
from heppy_fcc.particles.fcc.particle import Particle 

import math
from heppy_fcc.fastsim.simulator import Simulator
from heppy_fcc.fastsim.vectors import Point
from heppy_fcc.fastsim.pfobjects import Particle as PFSimParticle
from heppy_fcc.fastsim.toyevents import particles
from heppy_fcc.display.core import Display
from heppy_fcc.display.geometry import GDetector
from heppy_fcc.display.pfobjects import GTrajectories

from ROOT import TLorentzVector, TVector3

        
class PFSim(Analyzer):
    '''Runs PAPAS, the PArametrized Particle Simulation.

    Example configuration: 

    from heppy_fcc.analyzers.PFSim import PFSim
    from heppy_fcc.fastsim.detectors.CMS import CMS
    papas = cfg.Analyzer(
        PFSim,
        instance_label = 'papas',              
        detector = CMS(),
        gen_particles = 'gen_particles_stable',
        sim_particles = 'sim_particles',
        rec_particles = 'rec_particles',
        display = False,                   
        verbose = False
    )

    detector:      Detector model to be used. 
    gen_particles: Name of the input gen particle collection
    sim_particles: Name extension for the output sim particle collection. 
                   Note that the instance label is prepended to this name. 
                   Therefore, in this particular case, the name of the output 
                   sim particle collection is "papas_sim_particles".
    rec_particles: Name extension for the output reconstructed particle collection.
                   Same comments as for the sim_particles parameter above. 
    display      : Enable the event display
    verbose      : Enable the detailed printout.
    '''

    def __init__(self, *args, **kwargs):
        super(PFSim, self).__init__(*args, **kwargs)
        self.detector = self.cfg_ana.detector
        self.simulator = Simulator(self.detector,
                                   self.mainLogger)
        self.simname = '_'.join([self.instance_label,  self.cfg_ana.sim_particles])
        self.recname = '_'.join([self.instance_label,  self.cfg_ana.rec_particles])
        self.is_display = self.cfg_ana.display
        if self.is_display:
            self.init_display()        
        
    def init_display(self):
        self.display = Display(['xy','yz'])
        self.gdetector = GDetector(self.detector)
        self.display.register(self.gdetector, layer=0, clearable=False)
        self.is_display = True
        
    def process(self, event):
        event.simulator = self 
        if self.is_display:
            self.display.clear()
        pfsim_particles = []
        gen_particles = getattr(event, self.cfg_ana.gen_particles)
        self.simulator.simulate( gen_particles )
        pfsim_particles = self.simulator.ptcs
        if self.is_display:
            self.display.register( GTrajectories(pfsim_particles),
                                   layer=1)
        simparticles = sorted( pfsim_particles,
                               key = lambda ptc: ptc.e(), reverse=True)
        particles = sorted( self.simulator.particles,
                            key = lambda ptc: ptc.e(), reverse=True)
        setattr(event, self.simname, simparticles)
        setattr(event, self.recname, particles)
