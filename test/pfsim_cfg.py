import os
import heppy.framework.config as cfg
import logging
logging.basicConfig(level=logging.WARNING)

# input component 
# several input components can be declared,
# and added to the list of selected components
inputSample = cfg.Component(
    'albers_example',
    # files = ['zqq.root'],
    # files = ['ww.root'],
    # files = ['hz.root'],
    files = ['ttbar.root'],
    )

selectedComponents  = [inputSample]


from heppy_fcc.analyzers.PFSim import PFSim
pfsim = cfg.Analyzer(
    PFSim,
    verbose = True
)

# definition of a sequence of analyzers,
# the analyzers will process each event in this order
sequence = cfg.Sequence( [
    pfsim,
    ] )

# inputSample.files.append('albers_2.root')
# inputSample.splitFactor = 2  # splitting the component in 2 chunks

# finalization of the configuration object.
from ROOT import gSystem
gSystem.Load("libdatamodel")
from eventstore import EventStore as Events
config = cfg.Config(
    components = selectedComponents,
    sequence = sequence,
    services = [],
    events_class = Events
)

    
if __name__ == '__main__':
    from heppy.framework.looper import Looper
    import sys

    def process(iev=None):
        if iev is None:
            iev = loop.iEvent
        loop.process(iev)
        display.draw()

    def next():
        loop.process(loop.iEvent+1)
        display.draw()

    iev = int(sys.argv[1])
    loop = Looper( 'looper',
                   config,
                   1000, 0,
                   nPrint = 0,
                   timeReport = False,
                   quiet = True)

    pfsim = loop.analyzers[0]
    display = pfsim.display
    simulator = pfsim.simulator
    detector = simulator.detector
    process(iev)
