from heppy.framework.analyzer import Analyzer
from heppy_fcc.tools.genbrowser import GenBrowser

class UserWarning(Exception):
    pass

class GenAnalyzer(Analyzer):
    
    def process(self, event):
        genptcs = event.gen_particles
        event.electrons = [ptc for ptc in genptcs if abs(ptc.pdgid())==11
                           and ptc.status()==1]
        if len(event.electrons)>2:
            event.genbrowser = GenBrowser(event.gen_particles,
                                          event.gen_vertices)
            import pdb; pdb.set_trace()
