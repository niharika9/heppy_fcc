import os
import copy
import heppy.framework.config as cfg

comp = cfg.Component(
    'example',
    files = ['example.root']
)
selectedComponents = [comp]

from heppy_fcc.analyzers.FCCReader import FCCReader
source = cfg.Analyzer(
    FCCReader
)  

from ROOT import gSystem
gSystem.Load("libdatamodel")
from eventstore import EventStore as Events

from heppy_fcc.analyzers.JetClusterizer import JetClusterizer
gen_jets = cfg.Analyzer(
    JetClusterizer,
    instance_label = 'gen',
    particles = 'gen_particles_stable'
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
    verbose = False
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


# definition of a sequence of analyzers,
# the analyzers will process each event in this order
sequence = cfg.Sequence( [
    source,
    gen_jets,
    papas,
    papas_jets,
    papas_jet_match,
    papas_jet_tree
    ] )
 
config = cfg.Config(
    components = selectedComponents,
    sequence = sequence,
    services = [],
    events_class = Events
)
