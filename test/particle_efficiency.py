from cpyroot import *
from OfficialStyle import *

import sys 
import os 

class Efficiency(object):

    def __init__(self, name, tree):
        self.name = name
        self.tree = tree
        self.num = None
        self.denom = None
        self.eff = None
        
    def hname(self, name):
        return '_'.join([self.name, name])
        
    def project(self, var, cut, numcut, nbins, xmin, xmax):
        if cut == '':
            cut = '1'
        if self.num is None: 
            self.num = TH1F( self.hname('num'), self.name, nbins, xmin, xmax)
        else:
            self.num.Reset()
        self.num.Sumw2()
        sRed.formatHisto(self.num)
        if self.denom is None: 
            self.denom = TH1F( self.hname('denom'), self.name, nbins, xmin, xmax)
        else:
            self.denom.Reset()
        self.denom.Sumw2()
        sBlue.formatHisto(self.denom)
        if self.eff is None: 
            self.eff = TH1F( self.hname('eff'), self.name, nbins, xmin, xmax)
        else:
            self.eff.Reset()
        self.eff.Sumw2()
        sBlack.formatHisto(self.eff)
        hists = [self.num, self.denom, self.eff]
        for h in hists:
            h.SetTitle(self.name)
            h.GetXaxis().SetTitle(var)
            h.GetYaxis().SetTitle('efficiency')
        
        print 'denom: var = ', var, ' cut = ', cut
        self.tree.Project(self.denom.GetName(), var, cut)
        numcut = '({cut}) && ({numcut})'.format(cut=cut,
                                                numcut=numcut)
        print 'num: var = ', var, ' cut = ', numcut
        self.tree.Project(self.num.GetName(), var, numcut)
        self.eff.Divide(self.num, self.denom, 1, 1, 'B')
        self.eff.GetYaxis().SetRangeUser(0,1)

    
        
officialStyle(gStyle)

sample = sys.argv[1]

papas_rootfile = 'heppy_fcc.analyzers.ParticleTreeProducer.ParticleTreeProducer_papas_g2r/tree.root'
cms_rootfile = 'heppy_fcc.analyzers.ParticleTreeProducer.ParticleTreeProducer_cms_g2r/tree.root'

papas_rootfile = '/'.join([sample, papas_rootfile])
cms_rootfile = '/'.join([sample, cms_rootfile])

do_cms = os.path.isfile(cms_rootfile)

papas = Chain(papas_rootfile)
if do_cms:
    cms = Chain(cms_rootfile)


def efficiencies(name, tree):
    
    # e_eff = Efficiency('_'.join([name, 'e']), tree)
    # e_eff.project('ptc_e', '', 'ptc_match_e>0. && ptc_match_pdgid==ptc_pdgid', 20, 0, 5)

    pt_eff = Efficiency('_'.join([name, 'pt']), tree)
    # pt_eff.project('ptc_pt', 'abs(ptc_eta)<1.5', 'ptc_match_pt>0. && ptc_match_pdgid==ptc_pdgid', 20, 0, 20)
    pt_eff.project('ptc_pt', 'abs(ptc_theta)<1.', 'ptc_match_pt>0. && ptc_match_pdgid==ptc_pdgid', 100, 0, 10)

    eta_eff = Efficiency('_'.join([name, 'eta']), tree)
    eta_eff.project('ptc_theta', 'ptc_pt>2.', 'ptc_match_pt>0. && ptc_match_pdgid==ptc_pdgid', 100, -3, 3 )

    return [pt_eff, eta_eff]

papas_eff = efficiencies('papas', papas)
if do_cms:
    cms_eff = efficiencies('cms', cms)

c1 = TCanvas()
papas_eff[0].eff.Draw()
if do_cms:
    sBlue.formatHisto(cms_eff[0].eff)
    cms_eff[0].eff.Draw('same')

c2 = TCanvas()
papas_eff[1].eff.Draw()
if do_cms:
    sBlue.formatHisto(cms_eff[1].eff)
    cms_eff[1].eff.Draw('same')

# c3 = TCanvas()
# papas_eff[2].eff.Draw()
# if do_cms:
#     sBlue.formatHisto(cms_eff[2].eff)
#     cms_eff[2].eff.Draw('same')

# if do_cms:
#     pt_eff = Efficiency('_'.join(['cms1', 'pt']), cms)
#     pt_eff.project('ptc_pt', 'abs(ptc_eta)<1.5', 'ptc_match_211_pt>0.', 20, 0, 20)
#     pt_eff.eff.Draw()

    
#     pt_eff2 = Efficiency('_'.join(['cms2', 'pt']), cms)
#     pt_eff2.project('ptc_pt', 'abs(ptc_eta)<1.5', 'ptc_match_pt>0. && ptc_match_pdgid==130', 20, 0, 20)
#     pt_eff2.eff.Draw('same')

    
