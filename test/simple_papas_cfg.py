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
    files = ['example.root']
)
selectedComponents = [comp]


from heppy_fcc.analyzers.FCCReader import FCCReader
source = cfg.Analyzer(
    FCCReader
)  

from heppy_fcc.analyzers.ResonanceBuilder import ResonanceBuilder
ztomumu = cfg.Analyzer(
    ResonanceBuilder,
    'ztomumu',
    leg_collection = 'gen_particles_stable',
    filter_func = lambda x : abs(x.pdgid()) == 13,
    pdgid = 23,
)  

ztoee = cfg.Analyzer(
    ResonanceBuilder,
    'ztoee',
    leg_collection = 'gen_particles_stable',
    filter_func = lambda x : abs(x.pdgid()) == 11,
    pdgid = 23,
)  

higgstojj = cfg.Analyzer(
    ResonanceBuilder,
    'higgstojj',
    leg_collection = 'gen_jets_qcd',
    filter_func = lambda x : x.e()>10.,
    pdgid = 25,
)

from ROOT import gSystem
gSystem.Load("libdatamodel")
from eventstore import EventStore as Events

from heppy_fcc.analyzers.ParticlesForJets import ParticlesForJets
gen_particles_for_jets = cfg.Analyzer(
    ParticlesForJets,
    'gen_particles_for_jets',
    particles = 'gen_particles_stable',
    resonances = ['ztomumu']
)

from heppy_fcc.analyzers.Filter import Filter
gen_jets_qcd = cfg.Analyzer(
    Filter, 
    'gen_jets_qcd',
    input_objects = 'gen_jets',
    filter_func = lambda x : x.constituents[22].e()/x.e()<0.9
)

from heppy_fcc.analyzers.JetClusterizer import JetClusterizer
gen_jets = cfg.Analyzer(
    JetClusterizer,
    instance_label = 'gen',
    particles = 'gen_particles_for_jets'
)

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
    verbose = True
)

papas_jets = cfg.Analyzer(
    JetClusterizer,
    instance_label = 'papas', 
    particles = 'papas_rec_particles'
)

from heppy_fcc.analyzers.Matcher import Matcher
papas_jet_match = cfg.Analyzer(
    Matcher,
    instance_label = 'papas', 
    match_particles = 'gen_jets',
    particles = 'papas_jets'
)

from heppy_fcc.analyzers.JetTreeProducer import JetTreeProducer
papas_jet_tree = cfg.Analyzer(
    JetTreeProducer,
    instance_label = 'papas',
    tree_name = 'events',
    tree_title = 'jets',
    jets = 'papas_jets'
)


from heppy_fcc.analyzers.HiggsTreeProducer import HiggsTreeProducer
gen_higgs_tree = cfg.Analyzer(
    HiggsTreeProducer,
    tree_name = 'events',
    tree_title = 'higgs tree',
)



# definition of a sequence of analyzers,
# the analyzers will process each event in this order
sequence = cfg.Sequence( [
    source,
    ztomumu,
#     ztoee,
    gen_particles_for_jets, 
    gen_jets,
    gen_jets_qcd,
    higgstojj,
    gen_higgs_tree,
    papas,
    papas_jets,
    papas_jet_match,
    papas_jet_tree,
    ] )
 
config = cfg.Config(
    components = selectedComponents,
    sequence = sequence,
    services = [],
    events_class = Events
)

if __name__ == '__main__':
    import sys
    from heppy.framework.looper import Looper

    import random
    random.seed(0xdeadbeef)

    def process(iev=None):
        if iev is None:
            iev = loop.iEvent
        loop.process(iev)
        if display:
            display.draw()

    def next():
        loop.process(loop.iEvent+1)
        if display:
            display.draw()            

    iev = None
    if len(sys.argv)==2:
        papas.display = True
        iev = int(sys.argv[1])
        
    loop = Looper( 'looper', config,
                   nEvents=100,
                   nPrint=0,
                   timeReport=True)
    simulation = None
    for ana in loop.analyzers: 
        if hasattr(ana, 'display'):
            simulation = ana
    display = getattr(simulation, 'display', None)
    simulator = simulation.simulator
    detector = simulator.detector
    if iev is not None:
        process(iev)
    else:
        loop.loop()
        loop.write()
