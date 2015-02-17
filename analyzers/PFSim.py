from heppy.framework.analyzer import Analyzer
from heppy_fcc.particles.physicsobjects import Particle 

class PFSimOutput(object):
    def __init__(self):
        self.genparticles_stable = []

        
class PFSim(Analyzer):
    
    def beginLoop(self, setup):
        # call the function of the base class defining self.counters
        # and self.averages
        super(PFSim, self).beginLoop(setup)

    def process(self, event):

        # move the following to a gen particle analyzer at some point 
        store = event.input
        output = PFSimOutput()
        edmparticles = store.get("GenParticle")
        for ptc in edmparticles:
            if ptc.read().Core.Status == 1:
                output.genparticles_stable.append( Particle(ptc) )
        if self.cfg_ana.verbose:
            print 'stable/all particles = {s}/{a}'.format(s=len(output.genparticles_stable),
                                                          a=len(edmparticles))
