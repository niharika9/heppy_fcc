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
    files = ['ee_ttbar.root']
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
gSystem.Load("libdatamodel")
from eventstore import EventStore as Events

# in case we want to redo jet clustering, not used at the moment.
from heppy_fcc.analyzers.JetClusterizer import JetClusterizer
gen_jets = cfg.Analyzer(
    JetClusterizer,
    instance_label = 'gen_jets_reclustered',
    particles = 'gen_particles_stable'
)

# now treating electrons and muons transparently.
# could use the same modules to have a collection of electrons
# and a collection of muons 
from heppy_fcc.analyzers.Filter import Filter
leptons = cfg.Analyzer(
    Filter,
    output = 'leptons',
    input_objects = 'gen_particles_stable',
    filter_func = lambda ptc: ptc.pt()>30 and abs(ptc.pdgid()) in [11, 13]
)

from heppy_fcc.analyzers.LeptonAnalyzer import LeptonAnalyzer
from heppy_fcc.particles.isolation import Circle
iso_leptons = cfg.Analyzer(
    LeptonAnalyzer,
    output = 'iso_leptons',
    leptons = 'leptons',
    particles = 'gen_particles_stable',
    iso_area = Circle(0.4)
)

# need to remove jets corresponding to leptons

from heppy_fcc.analyzers.M3Builder import M3Builder
m3 = cfg.Analyzer(
    M3Builder,
    instance_label = 'gen_m3',
    jets = 'gen_jets', # see FCC reader
    filter_func = lambda x : x.pt()>30.
)

from heppy_fcc.analyzers.TTbarTreeProducer import TTbarTreeProducer
gen_tree = cfg.Analyzer(
    TTbarTreeProducer,
    jets = 'gen_jets',
    m3 = 'gen_m3',
    leptons = 'iso_leptons'
)

# definition of a sequence of analyzers,
# the analyzers will process each event in this order
sequence = cfg.Sequence( [
    source,
    # gen_jets,
    leptons,
    iso_leptons,
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
