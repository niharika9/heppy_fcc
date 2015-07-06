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

from heppy_fcc.analyzers.Recoil import Recoil
gen_recoil = cfg.Analyzer(
    Recoil,
    instance_label = 'gen',
    sqrts = 350.,
    particles = 'gen_particles_stable'
)

from heppy_fcc.analyzers.JetClusterizer import JetClusterizer
gen_jets = cfg.Analyzer(
    JetClusterizer,
    instance_label = 'gen',
    particles = 'gen_particles_stable'
)

# definition of a sequence of analyzers,
# the analyzers will process each event in this order
sequence = cfg.Sequence( [
    source,
    gen_recoil,
    gen_jets,
    ] )
 
config = cfg.Config(
    components = selectedComponents,
    sequence = sequence,
    services = [],
    events_class = Events
)
