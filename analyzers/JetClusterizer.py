from heppy.framework.analyzer import Analyzer
from heppy.framework.event import Event
from heppy_fcc.particles.physicsobjects import Particle 

from ROOT import gSystem
gSystem.Load("libanalysiscpp-tools")
from ROOT import JetClusterizer as CCJetClusterizer

import math

class Jet(object):
    
    def __init__(self, p4):
        self.p4 = p4
    def energy(self):
        return self.p4.E()
    def theta(self):
        return math.pi/2. - self.p4.Theta()
    def phi(self):
        return self.p4.Phi()
    def mass(self):
        return self.p4.M()
    def __repr__(self):
        tmp = '{className} : E = {energy:5.1f}, theta = {theta:5.2f}, phi = {phi:5.2f}, mass = {mass:5.2f}'
        return tmp.format( className = self.__class__.__name__,
                           energy = self.energy(),
                           theta = self.theta(),
                           phi = self.phi(),
                           mass = self.mass() )
    
class JetClusterizer(Analyzer):

    def __init__(self, *args, **kwargs):
        super(JetClusterizer, self).__init__(*args, **kwargs)
        self.clusterizer = CCJetClusterizer()
      
    def process(self, event):
        particles = getattr(event, self.cfg_ana.particles)
        self.clusterizer.clear();
        for ptc in particles:
            self.clusterizer.add_p4( ptc.p4 )
        self.clusterizer.clusterize()
        self.mainLogger.info( 'njets = {n}'.format(
            n=self.clusterizer.n_jets()))
        jets = []
        for jeti in range(self.clusterizer.n_jets()):
            jet = Jet( self.clusterizer.jet(jeti) )
            jets.append( jet )
            self.mainLogger.info( '\t{jet}'.format(jet=jet))
        event.jets = jets
