import os
import copy
import heppy.framework.config as cfg

import logging
# next 2 lines necessary to deal with reimports from ipython
logging.shutdown()
reload(logging)
logging.basicConfig(level=logging.WARNING)

comp = cfg.Component(
    'example',
    files = 'example.root'
)
selectedComponents = [comp]

from heppy_fcc.analyzers.FCCReader import FCCReader
source = cfg.Analyzer(
    FCCReader,
    mode = 'pp',
    gen_particles = 'GenParticle',
    gen_jets = 'GenJet',
)  

from ROOT import gSystem
gSystem.Load("libdatamodelDict")
from EventStore import EventStore as Events

from heppy_fcc.analyzers.METBuilder import METBuilder
gen_met = cfg.Analyzer(
    METBuilder,
    instance_label = 'gen_met',
    particles = 'gen_particles_stable'
)

# in case we want to redo jet clustering, not used at the moment.
from heppy_fcc.analyzers.JetClusterizer import JetClusterizer
gen_jets = cfg.Analyzer(
    JetClusterizer,
    instance_label = 'gen_jets_reclustered',
    particles = 'gen_particles_stable'
)

# currently treating electrons and muons transparently.
# could use the same modules to have a collection of electrons
# and a collection of muons 
from heppy_fcc.analyzers.Filter import Filter
leptons = cfg.Analyzer(
    Filter,
    'sel_leptons',
    output = 'leptons',
    input_objects = 'gen_particles_stable',
    filter_func = lambda ptc: ptc.pt()>30 and abs(ptc.pdgid()) in [11, 13]
)

from heppy_fcc.analyzers.LeptonAnalyzer import LeptonAnalyzer
from heppy_fcc.particles.isolation import EtaPhiCircle
iso_leptons = cfg.Analyzer(
    LeptonAnalyzer,
    leptons = 'leptons',
    particles = 'gen_particles_stable',
    iso_area = EtaPhiCircle(0.4)
)

#TODO: Colin: would be better to have a lepton class
def relative_isolation(lepton):
    sumpt = lepton.iso_211.sumpt + lepton.iso_22.sumpt + lepton.iso_130.sumpt
    sumpt /= lepton.pt()
    return sumpt

sel_iso_leptons = cfg.Analyzer(
    Filter,
    'sel_iso_leptons',
    output = 'sel_iso_leptons',
    input_objects = 'leptons',
    filter_func = lambda lep : relative_isolation(lep)<0.25
)

gen_jets_30 = cfg.Analyzer(
    Filter,
    'gen_jets_30',
    output = 'gen_jets_30',
    input_objects = 'gen_jets',
    filter_func = lambda jet: jet.pt()>30.
)

from heppy_fcc.analyzers.Matcher import Matcher
match_jet_leptons = cfg.Analyzer(
    Matcher,
    delta_r = 0.4,
    match_particles = 'sel_iso_leptons',
    particles = 'gen_jets_30'
)

sel_jets_nolepton = cfg.Analyzer(
    Filter,
    'sel_jets_nolepton',
    output = 'sel_jets_nolepton',
    input_objects = 'gen_jets_30',
    filter_func = lambda jet: not hasattr(jet, 'sel_iso_leptons')
)

from heppy_fcc.analyzers.M3Builder import M3Builder
m3 = cfg.Analyzer(
    M3Builder,
    instance_label = 'gen_m3',
    jets = 'sel_jets_nolepton', 
    filter_func = lambda x : x.pt()>30.
)

from heppy_fcc.analyzers.TTbarTreeProducer import TTbarTreeProducer
gen_tree = cfg.Analyzer(
    TTbarTreeProducer,
    jets = 'gen_jets',
    m3 = 'gen_m3',
    met = 'gen_met',
    leptons = 'leptons'
)



# definition of a sequence of analyzers,
# the analyzers will process each event in this order
sequence = cfg.Sequence( [
    source,
    # gen_jets,
    gen_met,
    leptons,
    iso_leptons,
    gen_jets_30,
    sel_iso_leptons,
    match_jet_leptons,
    sel_jets_nolepton,
    m3, 
    gen_tree
    ] )

# comp.files.append('example_2.root')
# comp.splitFactor = 2  # splitting the component in 2 chunks

config = cfg.Config(
    components = selectedComponents,
    sequence = sequence,
    services = [],
    events_class = Events
)

if __name__ == '__main__':
    import sys
    from heppy.framework.looper import Looper

    def next():
        loop.process(loop.iEvent+1)

    loop = Looper( 'looper', config,
                   nEvents=100,
                   nPrint=0,
                   timeReport=True)
    loop.process(6)
    print loop.event
