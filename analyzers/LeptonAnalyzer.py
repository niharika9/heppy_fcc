from heppy.framework.analyzer import Analyzer
from heppy.utils.deltar import matchObjectCollection, deltaR

class LeptonAnalyzer(Analyzer):

    def process(self, event):
        particles = getattr(event, self.cfg_ana.particles)            
        sel_leptons = [ptc for ptc in particles if self.sel_lepton(ptc)]
        for lepton in sel_leptons:
            print lepton
        
    def sel_lepton(self, ptc):
        if abs(ptc.pdgid()) == self.cfg_ana.pdgid:
            return True
