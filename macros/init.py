from cpyroot import * 

def init():
    import sys
    import os

    officialStyle(gStyle)
    
    sample = sys.argv[1]

    papas_rootfile = 'heppy_fcc.analyzers.ParticleTreeProducer.ParticleTreeProducer_papas_g2r/tree.root'
    cms_rootfile = 'heppy_fcc.analyzers.ParticleTreeProducer.ParticleTreeProducer_cms_g2r/tree.root'
    
    papas_rootfile = '/'.join([sample, papas_rootfile])
    cms_rootfile = '/'.join([sample, cms_rootfile])
    
    do_cms = os.path.isfile(cms_rootfile)
    
    papas = Chain(papas_rootfile)
    cms = Chain(cms_rootfile) if do_cms else None
    return papas, cms

        
