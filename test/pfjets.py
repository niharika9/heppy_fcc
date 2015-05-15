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

    
    
class FractionStack(object):

    def __init__(self, pdgids, hist):
        self.name = hist.GetName()
        self.hists = dict()
        self.pdgids= pdgids
        self.histsum = hist
        self.stack = THStack('_'.join([self.name, 'stack']), 'stack');
        colors = [2, 4, 8, 1, 1]
        for iid, pdgid in enumerate(self.pdgids):
            hname = '_'.join([self.name, str(pdgid)])
            hist = hist.Clone(hname)
            self.hists[pdgid] = hist
            hist.SetFillColor(colors[iid])
            self.stack.Add(self.hists[pdgid])
        self.histsum.SetLineWidth(3)
        self.histsum.SetLineColor(1)

            
    def Draw(self, tree, var, basecut='1'):
        tree.Project(self.histsum.GetName(), var, basecut)
        same = 'same'
        for pdgid in self.pdgids:
            jet = var.split('_')[0]
            compe = '_'.join([jet, str(pdgid), 'e'])
            jete = '_'.join([jet, 'e'])
            frac = '/'.join([compe, jete])
            cutfrac = '{frac}>0'.format(frac=frac)
            cut = '{frac}*({basecut} && {cutfrac})'.format(
                basecut = basecut,
                cutfrac = cutfrac,
                frac = frac
            )
            print 'var', var
            print 'cut', cut
            tree.Project(self.hists[pdgid].GetName(), var, cut)
            # self.hists[pdgid].Draw(same)
            # if same == '':
            #     same = 'same'
        self.stack.Draw()
        self.histsum.Draw('same')

c1 = TCanvas()
res_stack = FractionStack([211,22,130, 11, 13], TH1F('res', '', 100, 0, 2))
res_stack.Draw(tree, 'jet1_e / jet1_gen_e', 'jet1_e > 0')

# c2 = TCanvas()
# theta_stack = FractionStack([211,22,130, 11, 13], TH1F('theta', '', 20, -2, 2))
# theta_stack.Draw(tree, 'jet1_theta', 'jet1_gen_e>0')

                
