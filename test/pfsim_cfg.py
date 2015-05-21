import os
import heppy.framework.config as cfg

# input component 
# several input components can be declared,
# and added to the list of selected components

gen_jobs = None
do_display = True
nevents_per_job = 20000

if gen_jobs>1:
    do_display = False

inputSample = cfg.Component(
    'albers_example',
    files = ['example.root']
    # files = ['zqq.root'],
    # files = ['ww.root'],
    # files = ['hz.root'],
    # files = ['ttbar.root'],
    )

selectedComponents  = [inputSample]

if gen_jobs:
    selectedComponents = []
    for i in range(gen_jobs):
        component = cfg.Component(''.join(['sample_Chunk',str(i)]), files=['dummy.root'])
        selectedComponents.append(component)
        
    
from heppy_fcc.analyzers.FCCReader import FCCReader
reader = cfg.Analyzer(
    FCCReader
)

from heppy_fcc.analyzers.Gun import Gun
gun = cfg.Analyzer(
    Gun
)

from heppy_fcc.analyzers.PFSim import PFSim
pfsim = cfg.Analyzer(
    PFSim,
    display = do_display,
    verbose = True
)


from heppy_fcc.analyzers.JetClusterizer import JetClusterizer
jets = cfg.Analyzer(
    JetClusterizer,
    instance_label = 'rec',
    particles = 'particles'
)

genjets = cfg.Analyzer(
    JetClusterizer,
    instance_label = 'gen',
    particles = 'gen_particles_stable'
)

from heppy_fcc.analyzers.JetAnalyzer import JetAnalyzer
jetana = cfg.Analyzer(
    JetAnalyzer,
)


from heppy_fcc.analyzers.JetTreeProducer import JetTreeProducer
tree = cfg.Analyzer(
    JetTreeProducer,
    tree_name = 'events',
    tree_title = 'jets'
)


# definition of a sequence of analyzers,
# the analyzers will process each event in this order
sequence = cfg.Sequence( [
    gun if gen_jobs else reader,
    pfsim,
    jets,
    genjets,
    jetana,
    tree
    ] )

# inputSample.files.append('albers_2.root')
# inputSample.splitFactor = 2  # splitting the component in 2 chunks

# finalization of the configuration object.
from ROOT import gSystem
gSystem.Load("libdatamodel")
from eventstore import EventStore as Events
if gen_jobs:
    from heppy.framework.eventsgen import Events 
config = cfg.Config(
    components = selectedComponents,
    sequence = sequence,
    services = [],
    events_class = Events
)

    
if __name__ == '__main__':
    import sys
    from heppy.framework.looper import Looper
    import logging

    # next 2 lines necessary to deal with reimports from ipython
    logging.shutdown()
    reload(logging)
    logging.basicConfig(level=logging.ERROR)

    import random
    # for reproducible results
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
        iev = int(sys.argv[1])
    loop = Looper( 'looper', config,
                   nEvents=nevents_per_job,
                   nPrint=5,
                   timeReport=True)
    pfsim = loop.analyzers[1]
    display = getattr(pfsim, 'display', None)
    simulator = pfsim.simulator
    detector = simulator.detector
    if iev is not None:
        process(iev)
    else:
        loop.loop()
        loop.write()
