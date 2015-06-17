import os
import copy
import heppy.framework.config as cfg

debug = False

do_display = False
do_cms = True
do_papas = True
nevents_per_job = 1000

# from heppy_fcc.samples.higgs_350 import *  
from heppy_fcc.samples.gun_0_50 import gun_22_0_50 as sample
selectedComponents  = [sample]
for comp in selectedComponents:
    comp.splitFactor = 10
if debug:
    selectedComponents = selectedComponents[:1]
    selectedComponents[0].splitFactor =1 

from heppy_fcc.analyzers.CMSReader import CMSReader
source = cfg.Analyzer(
    CMSReader,
    gen_particles = 'genParticles',
    pf_particles = 'particleFlow' if do_cms else None
    )


from heppy_fcc.analyzers.Recoil import Recoil
gen_recoil = cfg.Analyzer(
    Recoil,
    instance_label = 'gen',
    sqrts = 350.,
    particles = 'gen_particles_stable'
)

from heppy_fcc.analyzers.PFSim import PFSim
pfsim = cfg.Analyzer(
    PFSim,
    display = do_display,
    verbose = False
)


# cms_recoil = cfg.Analyzer(
#     Recoil,
#     instance_label = 'cms',
#     sqrts = 350.,
#     particles = 'pf_particles'
# )

papas_recoil = cfg.Analyzer(
    Recoil,
    instance_label = 'papas',
    sqrts = 350.,
    particles = 'particles'
)

from heppy_fcc.analyzers.Matcher import Matcher
papas_particle_match_r2g = cfg.Analyzer(
    Matcher,
    instance_label = 'papas_r2g', 
    particles = 'particles',
    match_particles = 'gen_particles_stable'
)

papas_particle_match_g2r = cfg.Analyzer(
    Matcher,
    instance_label = 'papas_g2r', 
    particles = 'gen_particles_stable',
    match_particles = 'particles'
)

from heppy_fcc.analyzers.ParticleTreeProducer import ParticleTreeProducer
papas_particle_tree_r2g = cfg.Analyzer(
    ParticleTreeProducer, 
    instance_label = 'papas_r2g',
    particles = 'particles'
    )
papas_particle_tree_g2r = cfg.Analyzer(
    ParticleTreeProducer, 
    instance_label = 'papas_g2r',
    particles = 'gen_particles_stable'
    )

from heppy_fcc.analyzers.Higgs350TreeProducer import Higgs350TreeProducer
papas_tree = cfg.Analyzer(
    Higgs350TreeProducer,
    instance_label = 'papas'
    )

papas_sequence = [
    papas_recoil,
    papas_particle_match_r2g,
    papas_particle_match_g2r,
    papas_tree, 
    papas_particle_tree_r2g,
    papas_particle_tree_g2r,      
    ]


cms_recoil = cfg.Analyzer(
    Recoil,
    instance_label = 'cms',
    sqrts = 350.,
    particles = 'pf_particles'
)

from heppy_fcc.analyzers.Matcher import Matcher
cms_particle_match_r2g = cfg.Analyzer(
    Matcher,
    instance_label = 'cms_r2g', 
    particles = 'pf_particles',
    match_particles = 'gen_particles_stable'
)

cms_particle_match_g2r = cfg.Analyzer(
    Matcher,
    instance_label = 'cms_g2r', 
    particles = 'gen_particles_stable',
    match_particles = 'pf_particles'
)

from heppy_fcc.analyzers.ParticleTreeProducer import ParticleTreeProducer
cms_particle_tree_r2g = cfg.Analyzer(
    ParticleTreeProducer, 
    instance_label = 'cms_r2g',
    particles = 'pf_particles'
    )
cms_particle_tree_g2r = cfg.Analyzer(
    ParticleTreeProducer, 
    instance_label = 'cms_g2r',
    particles = 'gen_particles_stable'
    )

from heppy_fcc.analyzers.Higgs350TreeProducer import Higgs350TreeProducer
cms_tree = cfg.Analyzer(
    Higgs350TreeProducer,
    instance_label = 'cms'
    )

cms_sequence = [
    cms_recoil,
    cms_particle_match_r2g,
    cms_particle_match_g2r,
    cms_tree, 
    cms_particle_tree_r2g,
    cms_particle_tree_g2r,      
    ]

# definition of a sequence of analyzers,
# the analyzers will process each event in this order
sequence = cfg.Sequence( [
    source,
    pfsim,
    gen_recoil, 
    ] )

if do_papas:
    sequence.extend(papas_sequence)
if do_cms:
    sequence.extend(cms_sequence)
    

from PhysicsTools.HeppyCore.framework.eventsfwlite import Events
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
                   nPrint=0,
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
