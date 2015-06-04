from ROOT import *
from ROOT import gDirectory
from OfficialStyle import *

import sys 

officialStyle(gStyle)

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
        self.stack = THStack('_'.join([self.name, 'stack']),
                             hist.GetTitle());
        colors = [2, 4, 8, 1, 1]
        for iid, pdgid in enumerate(self.pdgids):
            hname = '_'.join([self.name, str(pdgid)])
            hist = hist.Clone(hname)
            self.hists[pdgid] = hist
            hist.SetFillColor(colors[iid])
            hist.SetFillStyle(1001)
            self.stack.Add(self.hists[pdgid])
        self.histsum.SetLineWidth(1)
        self.histsum.SetLineColor(1)
            
    def Project(self, tree, var, basecut='1'):
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
            print self.hists[pdgid].GetName()
            tree.Project(self.hists[pdgid].GetName(), var, cut)
            # self.hists[pdgid].Draw(same)
            # if same == '':
            #     same = 'same'
        self.Draw()

    def Draw(self):
        self.histsum.Draw('hist')
        self.stack.Draw("histsame")
        self.histsum.Draw('histsame')
        gPad.RedrawAxis()

    def SetYRange(self, min, max):
        self.histsum.GetYaxis().SetRangeUser(min, max)
        self.Draw()

        
pdgids = [211,22,130, 11, 13]
        
def prepare_tree(tree):
    for pdgid in pdgids:
        tree.SetAlias("jet1_{pdgid}_frac".format(pdgid=pdgid),
                      "jet1_{pdgid}_e/jet1_e".format(pdgid=pdgid))
        tree.SetAlias("jet1_gen_{pdgid}_frac".format(pdgid=pdgid),
                      "jet1_gen_{pdgid}_e/jet1_gen_e".format(pdgid=pdgid))
    elist = TEventList("elist")
    tree.Draw(">>elist", "jet1_gen_211_e>0 && abs(jet1_gen_eta)<2. && abs(jet1_gen_pt>2.)")
    tree.SetEventList(elist)
    
prepare_tree(tree)

c1 = TCanvas()
res_stack = FractionStack(pdgids, TH1F('res', ';E/E_{gen} (GeV)', 50, 0, 2))
res_stack.Project(tree, 'jet1_e / jet1_gen_e', 'jet1_e > 0')
res_stack.SetYRange(50, 50000)

double_count = res_stack.histsum.Clone("double_count")
double_count.SetLineStyle(2)
double_count.SetLineWidth(3)
double_count.SetLineColor(0)
tree.Draw("jet1_e/jet1_gen_e>>double_count","jet1_211_frac>0. && jet1_211_frac<1.","same")

missed = double_count.Clone("missed")
missed.SetLineColor(5)
tree.Draw("jet1_e/jet1_gen_e>>missed","jet1_211_frac==0.","same")

pure = double_count.Clone("pure")
pure.SetLineColor(kGray)
tree.Draw("jet1_e/jet1_gen_e>>pure","jet1_211_frac==1.","same")

gPad.RedrawAxis()

ntot = res_stack.histsum.GetEntries()
nmissed = missed.GetEntries()
ndouble = double_count.GetEntries() 
npure = pure.GetEntries()
nseen = ntot - nmissed
eff = nseen / ntot
ineff = nmissed / ntot
dcount_prob = ndouble / ntot
pure_prob = npure / ntot
print 'eff = ', eff
print 'missed = ', ineff
print 'dcount_prob = ', dcount_prob
print 'pure = ', pure_prob

c1.SetLogy()

# c2 = TCanvas()
# theta_stack = FractionStack(pdgids, TH1F('theta', '', 20, -2, 2))
# theta_stack.Draw(tree, 'jet1_theta', 'jet1_gen_e>0')

                
# c3 = TCanvas()
# pt_stack = FractionStack(pdgids, TH1F('pt', '', 20, 0, 20))
# pt_stack.Project(tree, 'jet1_gen_pt', 'jet1_e > 0 && abs(jet1_eta)<1.')

