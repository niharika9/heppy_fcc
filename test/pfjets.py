from ROOT import *

import sys 

rootfile = 'heppy_fcc.analyzers.JetTreeProducer.JetTreeProducer_1/jet_tree.root'

directory = sys.argv[1]

rfile = TFile('/'.join([directory, rootfile]))
tree = rfile.Get('events')

def hn(name, hname):
    return '_'.join([name, hname]) 


class Histo(object):
    
    def __init__(self, tree, name, var, cut, nbins, xmin, xmax):
        self.h = TH1F( name, name, nbins, xmin, xmax)
        tree.Project(name, var, cut)

    def __getattr__(self, attr):
        return getattr(self.h, attr)

        
jet1_e = Histo(tree, 'jet1_e', 'jet1_e', '', 100, 0, 100)
jet1_e.Draw()

jet1_de = Histo(tree, 'response', 'jet1_e/jet1_gen_e', '', 100, 0, 2)
jet1_de.Draw()


pdgids = [211, 22, 130]
dfrac_pdgid = dict()
frac_pdgid = dict()
frac_pdgid_gen = dict()
for pdgid in pdgids:
    frac_pdgid[pdgid] = Histo(tree,
                              'frac_{id}'.format(id=pdgid),
                              'jet1_{id}_e/jet1_e'.format(id=pdgid),
                              '', 100, 0, 2)
    frac_pdgid_gen[pdgid] = Histo(tree,
                                  'frac_gen_{id}'.format(id=pdgid),
                                  'jet1_gen_{id}_e/jet1_gen_e'.format(id=pdgid),
                                  '', 100, 0, 2)
    


