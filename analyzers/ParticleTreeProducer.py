from heppy.framework.analyzer import Analyzer
from heppy.statistics.tree import Tree
from heppy_fcc.analyzers.ntuple import *

from ROOT import TFile

class ParticleTreeProducer(Analyzer):

    def beginLoop(self, setup):
        super(ParticleTreeProducer, self).beginLoop(setup)
        self.rootfile = TFile('/'.join([self.dirName,
                                        'tree.root']),
                              'recreate')
        self.tree = Tree('particles', '')
        bookParticle(self.tree, 'ptc')
        bookParticle(self.tree, 'ptc_match')
        
    def process(self, event):
        particles = getattr(event, self.cfg_ana.particles)
        for ptc in particles: 
            self.tree.reset()
            fillParticle(self.tree, 'ptc', ptc)
            if ptc.match:
                fillParticle(self.tree, 'ptc_match', ptc.match)
            self.tree.tree.Fill()
        
        
    def write(self, setup):
        self.rootfile.Write()
        self.rootfile.Close()
        
