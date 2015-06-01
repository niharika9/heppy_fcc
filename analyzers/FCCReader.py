from heppy.framework.analyzer import Analyzer
from heppy_fcc.particles.fcc.particle import Particle 
from heppy_fcc.particles.fcc.vertex import Vertex 
from heppy_fcc.tools.genbrowser import GenBrowser

import math
import pprint

class FCCReader(Analyzer):
    
    def process(self, event):
        store = event.input
        gen_vertices = store.get("GenVertex")
        event.gen_vertices = map(Vertex, gen_vertices)
        gen_particles = map(Particle, store.get("GenParticle"))
        event.gen_particles = sorted( gen_particles,
                                      key = lambda ptc: ptc.e(),
                                      reverse=True )  
        event.gen_particles_stable = [ptc for ptc in event.gen_particles
                                      if ptc.status()==1 and \
                                      not math.isnan(ptc.e())]
        # event.genbrowser = GenBrowser(event.gen_particles, event.gen_vertices)
