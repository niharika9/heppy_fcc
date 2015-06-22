from cpyroot import *
from OfficialStyle import *
from heppy.statistics.value import Value

import sys 
import os 

class Resolution(object):

    def __init__(self, name, tree):
        self.name = name
        self.tree = tree
        self.h2d = None
        
    def hname(self, name):
        return '_'.join([self.name, name])
        
    def project(self, var, cut, nbins, xmin, xmax, ynbins, ymin, ymax):
        if self.h2d is None: 
            self.h2d = TH2F( self.hname('h2d'), self.name,
                             nbins, xmin, xmax,
                             ynbins, ymin, ymax)
        else:
            self.h2d.Reset()
        self.h2d.SetTitle(self.name)
        vary, varx = var.split(':')
        self.h2d.GetXaxis().SetTitle(varx)
        self.h2d.GetYaxis().SetTitle(vary)

        print vary
        print varx
        print cut
        
        self.tree.Project(self.h2d.GetName(), var, cut)
        # self.h2d.Draw('colz')
        self.fit()

    def fit_slice(self, ibin, draw=True, nentries_min=20):
        self.proj = self.h2d.ProjectionY('',ibin,ibin,'')
        if self.proj.GetEntries()<nentries_min:
            return None, None
        opt = 'Q' if draw else 'Q0'
        self.proj.Fit('gaus', opt)
        func = self.proj.GetFunction('gaus')
        mean = Value( func.GetParameter(1),
                      func.GetParError(1))
        sigma = Value( func.GetParameter(2), 
                       func.GetParError(2))
        print ibin
        print mean
        print sigma
        return mean, sigma

    def fit(self):
        self.hmean = self.h2d.ProjectionX().Clone('hmean')
        self.hmean.Reset()
        self.hmean.SetYTitle('relative scale')
        self.hsigma = self.h2d.ProjectionX().Clone('hsigma')
        self.hsigma.Reset()
        self.hsigma.SetYTitle('relative resolution')
        for ibin in range(self.h2d.GetNbinsX()):
            mean, sigma = self.fit_slice(ibin+1, False)
            if mean and sigma: 
                self.hmean.SetBinContent(ibin, mean.val)
                self.hmean.SetBinError(ibin, mean.err)
                self.hsigma.SetBinContent(ibin, sigma.val)
                self.hsigma.SetBinError(ibin, sigma.err)

    def draw_2d(self):
        self.h2d.Draw('colz')
        self.hmean.Draw('same')
        
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

papas_res_e = Resolution('papas_res_e', papas)
papas_res_e.project('ptc_match_e/ptc_e:ptc_e', 'ptc_match_pdgid == ptc_pdgid',
                    20, 0, 5, 50, 0.9, 1.1)
# papas_res_e.fit_slice(10)
papas_res_e.draw_2d()
