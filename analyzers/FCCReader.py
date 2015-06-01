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
        # for v in gen_vertices:
        #    event.gen_vertices.append(v.read())
        gen_particles = map(Particle, store.get("GenParticle"))
        event.gen_particles = sorted( gen_particles,
                                      key = lambda ptc: ptc.e(), reverse=True )  
        event.gen_particles_stable = [ptc for ptc in event.gen_particles
                                      if ptc.status()==1 and not math.isnan(ptc.e())]
        # import pdb; pdb.set_trace()
        event.genbrowser = GenBrowser(event.gen_particles, event.gen_vertices)

        # vdict = dict.fromkeys(event.gen_vertices, True)
        # for v in vdict:
        #     print v, hash(v), v.fccvertex.index()
        # for p in event.gen_particles:
        #     if p.start_vertex():
        #         print '\t', p.start_vertex(), hash(p.start_vertex()), p.start_vertex().fccvertex.index(),  p.start_vertex().fccvertex.containerID()
        #         print 'inside dict', vdict.get(p.start_vertex(), False)
        #         import pdb; pdb.set_trace()
            # if p.start_vertex():
            #     try:
            #         print 'start is in', p.start_vertex() in vdict
            #         print vdict[p.start_vertex()] 
            #     except KeyError:
            #         import pdb; pdb.set_trace()
