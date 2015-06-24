import os
import copy
import heppy.framework.config as cfg

debug = False
do_display = False
do_cms = True
do_papas = True
nevents_per_job = 1000
gen_jobs = 4

GEN = gen_jobs>0

if debug:
    print 'DEBUG MODE IS ON!'

source = None
selectedComponents = []
Events = None
if GEN:
    do_cms = False
    do_papas = True
    for i in range(gen_jobs):
        component = cfg.Component(''.join(['sample_Chunk',str(i)]), files=['dummy.root'])
        selectedComponents.append(component)
    from heppy_fcc.analyzers.Gun import Gun
    source = cfg.Analyzer(
        Gun,
        pdgid = 130,
        ptmin = 0.7,
        ptmax = 20.,
        thetamin = -1.5,
        thetamax = 1.5,
        flat_pt = False
    )
    from heppy.framework.eventsgen import Events
else:
    # from heppy_fcc.samples.higgs_350 import *  
    from heppy_fcc.samples.gun import *
    # from heppy_fcc.samples.gun_MatEff_10_50 import *
    # selectedComponents = [gun_22_0_50]
    # selectedComponents = [gun_22_0_50_eta3]
    selectedComponents = [gun_130_007_20]
    for comp in selectedComponents:
        comp.splitFactor = 10

    from heppy_fcc.analyzers.CMSReader import CMSReader
    source = cfg.Analyzer(
        CMSReader,
        gen_particles = 'genParticles',
        pf_particles = 'particleFlow' if do_cms else None
    )
    from PhysicsTools.HeppyCore.framework.eventsfwlite import Events

if debug:
    comp = selectedComponents[0]
    comp.splitFactor =1 
    # comp.files = selectedComponents[0].files[:1]
    # comp.files = ['gun_211_0to10_ME0_RECOSIM.root'] 
    selectedComponents = [comp]

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

from heppy_fcc.analyzers.PFSim import PFSim
pfsim = cfg.Analyzer(
    PFSim,
    display = do_display,
    verbose = False
)


papas_jets = cfg.Analyzer(
    JetClusterizer,
    instance_label = 'papas', 
    particles = 'particles'
)

from heppy_fcc.analyzers.JetAnalyzer import JetAnalyzer
papas_jet_ana = cfg.Analyzer(
    JetAnalyzer,
    instance_label = 'papas', 
    jets = 'papas_jets',
    genjets = 'gen_jets'
)

from heppy_fcc.analyzers.JetTreeProducer import JetTreeProducer
papas_jet_tree = cfg.Analyzer(
    JetTreeProducer,
    instance_label = 'papas',
    tree_name = 'events',
    tree_title = 'jets',
    jets = 'papas_jets'
)

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
    match_particles = [
        ('particles', None),
        ('particles', 211),
        ('particles', 130),
        ('particles', 22)
    ] 
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
    pfsim, 
    papas_jets, 
    papas_jet_ana,
    papas_jet_tree,
    papas_recoil,
    # papas_particle_match_r2g,
    papas_particle_match_g2r,
    papas_tree, 
    # papas_particle_tree_r2g,
    papas_particle_tree_g2r,      
    ]


from heppy_fcc.analyzers.FastsimCleaner import FastsimCleaner 
cms_fastsim_cleaner = cfg.Analyzer(
    FastsimCleaner, 
    particles = 'pf_particles'
)

cms_jets = cfg.Analyzer(
    JetClusterizer,
    instance_label = 'cms', 
    particles = 'pf_particles'
)

cms_jet_ana = cfg.Analyzer(
    JetAnalyzer,
    instance_label = 'cms', 
    jets = 'cms_jets',
    genjets = 'gen_jets'
)

cms_jet_tree = cfg.Analyzer(
    JetTreeProducer,
    instance_label = 'cms',
    tree_name = 'events',
    tree_title = 'jets',
    jets = 'cms_jets'
)


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
    match_particles = [
        ('pf_particles', None),
        ('pf_particles', 211),
        ('pf_particles', 130)
    ] 
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
    cms_fastsim_cleaner,
    cms_jets, 
    cms_jet_ana,
    cms_jet_tree,
    cms_recoil,
    # cms_particle_match_r2g,
    cms_particle_match_g2r,
    cms_tree, 
    # cms_particle_tree_r2g,
    cms_particle_tree_g2r,      
    ]

# definition of a sequence of analyzers,
# the analyzers will process each event in this order
sequence = cfg.Sequence( [
    source,
    gen_recoil,
    gen_jets,
    ] )

if do_papas:
    sequence.extend(papas_sequence)
if do_cms:
    sequence.extend(cms_sequence)

# sequence = cfg.Sequence([source])

# sequence = cfg.Sequence(
#    [source, cms_fastsim_cleaner]
#)
    
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
    logging.basicConfig(level=logging.INFO)

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
    # pfsim = loop.analyzers[1]
    # display = getattr(pfsim, 'display', None)
    display = None
    # simulator = pfsim.simulator
    # detector = simulator.detector
    if iev is not None:
        process(iev)
    else:
        loop.loop()
        loop.write()
