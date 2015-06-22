from cpyroot import *
from OfficialStyle import *
from heppy.statistics.value import Value

import sys 
import os 

class Resolution(object):

    def __init__(self, name, tree, style=sBlack):
        self.name = name
        self.tree = tree
        self.h2d = None
        self.style = style
        
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
        opt = '' if draw else 'Q0'
        self.style.formatHisto(self.proj)
        self.proj.Fit('gaus', opt)
        func = self.proj.GetFunction('gaus')
        mean = Value( func.GetParameter(1),
                      func.GetParError(1))
        sigma = Value( func.GetParameter(2), 
                       func.GetParError(2))
        return mean, sigma

    def fit(self):
        self.hmean = self.h2d.ProjectionX().Clone('hmean')
        self.hmean.Reset()
        self.hmean.SetYTitle('relative scale')
        self.style.formatHisto(self.hmean)
        self.hsigma = self.h2d.ProjectionX().Clone('hsigma')
        self.hsigma.Reset()
        self.hsigma.SetYTitle('relative resolution')
        self.style.formatHisto(self.hsigma)
        for ibin in range(self.h2d.GetNbinsX()):
            ii = ibin+1
            mean, sigma = self.fit_slice(ii, False)
            if mean and sigma: 
                self.hmean.SetBinContent(ii, mean.val)
                self.hmean.SetBinError(ii, mean.err)
                self.hsigma.SetBinContent(ii, sigma.val)
                self.hsigma.SetBinError(ii, sigma.err)
        self.fit_res()
                
    def fit_res(self, draw=True):
        func = TF1(self.hname('res_calo'),
                   'sqrt( ([0]/sqrt(x))**2 + ([1]/x)**2 ) + [2]**2 ')
        func.SetParLimits(0, 0., 9999999.)
        func.SetParLimits(1, 0., 9999999.)
        func.SetParLimits(2, 0., 9999999.)
        opt = '' if draw else 'Q0'
        self.hsigma.Fit(self.hname('res_calo'), opt)
        stoch = Value( func.GetParameter(0), func.GetParError(0))
        noise = Value( func.GetParameter(1), func.GetParError(1))
        const = Value( func.GetParameter(2), func.GetParError(2))
        print stoch, noise, const
        return stoch, noise, const
        
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
                    50, 0.3, 20, 50, 0.9, 1.1)
# papas_res_e.fit_slice(10)
# papas_res_e.draw_2d()

if do_cms:
    cms_res_e = Resolution('cms_res_e', cms, style=sBlue)
    cms_res_e.project('ptc_match_e/ptc_e:ptc_e', 'ptc_match_pdgid == ptc_pdgid',
                      50, 0.3, 20, 50, 0.9, 1.1)
    cms_res_e.hsigma.Draw()

    
papas_res_e.hsigma.Draw('same')
