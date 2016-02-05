from heppy.framework.analyzer import Analyzer
from heppy.utils.deltar import matchObjectCollection, deltaR
from heppy_fcc.particles.isolation import Isolation

class LeptonAnalyzer(Analyzer):

    def beginLoop(self, setup):
        super(LeptonAnalyzer, self).beginLoop(setup)
    
    def process(self, event):
        leptons = self.cfg_ana.leptons
        particles = getattr(event, self.cfg_ana.particles)
        leptons = getattr(event, self.cfg_ana.leptons)
        pdgids = [211, 22, 130]
        for lepton in leptons:
            for pdgid in pdgids:
                self.set_isolation(lepton, particles, pdgid)
        setattr(event, self.cfg_ana.output, leptons)

    def set_isolation(self, lepton, particles, pdgid):
        sel_ptcs = [ptc for ptc in particles if ptc.pdgid()==pdgid]
        iso = Isolation(lepton, sel_ptcs, [self.cfg_ana.iso_area],
                        label=str(pdgid))
        setattr(lepton, 'iso_{pdgid}'.format(pdgid=pdgid), iso)
        
