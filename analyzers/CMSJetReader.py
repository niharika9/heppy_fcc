from PhysicsTools.Heppy.analyzers.core.Analyzer import Analyzer
from PhysicsTools.Heppy.analyzers.core.AutoHandle import AutoHandle
from heppy_fcc.particles.cms.jet import Jet

import math

class CMSJetReader(Analyzer):
    
    def declareHandles(self):
        super(CMSJetReader, self).declareHandles()
        self.handles['jets'] = AutoHandle(
            self.cfg_ana.jets, 
            'std::vector<reco::PFJet>'
            )
        self.handles['gen_jets'] = AutoHandle(
            self.cfg_ana.gen_jets, 
            'std::vector<reco::GenJet>'
            )

    def process(self, event):
        self.readCollections(event.input)
        store = event.input
        genj = self.handles['gen_jets'].product()
        genj = [jet for jet in genj if jet.pt()>self.cfg_ana.gen_jet_pt]
        gen_jets = map(Jet, genj)
        # gen_jets = [jet for jet in gen_jets if jet.pt()>self.cfg_ana.gen_jet_pt]
        event.gen_jets = sorted( gen_jets,
                                 key = lambda ptc: ptc.pt(), reverse=True )  
        
        for jet in event.gen_jets:
            jet.constituents.validate(jet.e())
