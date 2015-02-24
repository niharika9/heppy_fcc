from heppy_fcc.fastsim.propagator import StraightLinePropagator, HelixPropagator 
from heppy_fcc.fastsim.pfobjects import Cluster
import random

class Simulator(object):

    def __init__(self, detector):
        self.detector = detector
        self.prop_helix = HelixPropagator()
        self.prop_straight = StraightLinePropagator()
        
    def reset(self):
        self.particles = None
        Cluster.max_energy = 0.

    def propagator(self, ptc):
        is_neutral = abs(ptc.charge)<0.5
        return self.prop_straight if is_neutral else self.prop_helix
        
    def propagate(self, ptc):
        '''propagate the particle to all dector cylinders'''
        self.propagator(ptc).propagate([ptc], self.detector.cylinders(),
                                       self.detector.elements['field'].magnitude)

    def make_cluster(self, ptc, detname, fraction=1., size=None):
        '''adds a cluster in a given detector, with a given fraction of 
        the particle energy.'''
        detector = self.detector.elements[detname]
        self.propagator(ptc).propagate_one(ptc,
                                           detector.volume.inner,
                                           self.detector.elements['field'].magnitude )
        if size is None:
            size = detector.cluster_size(ptc)
        cylname = detector.volume.inner.name
        ptc.clusters[cylname] = Cluster(ptc.p4.E()*fraction,
                                        ptc.points[cylname],
                                        size,
                                        cylname, ptc)

    def simulate_photon(self, ptc):
        # true deposit:
        # straight extrapolation to ECAL
        # EM deposit all energy
        ecal = self.detector.elements['ecal']
        self.prop_straight.propagate_one(ptc,
                                         ecal.volume.inner)
        
        self.make_cluster(ptc, 'ecal')

    def reconstruct_photon(self, ptc):
        # create reconstructed EM deposit
        # acceptance
        # possibly smear position EM
        # apply E thresh
        # smear energy EM
        pass

    def simulate_electron(self, ptc):
        # true deposit
        # helix extrapolation to ECAL
        # EM deposit all energy
        ecal = self.detector.elements['ecal']
        self.prop_helix.propagate_one(ptc,
                                      ecal.volume.inner,
                                      self.detector.elements['field'].magnitude )
        self.make_cluster(ptc, 'ecal')

    def reconstruct_electron(self, ptc):
        # create reconstructed EM deposit
        # possibly smear position EM
        # smear energy EM        
        pass

        
    def simulate_hadron(self, ptc):
        ecal = self.detector.elements['ecal']
        path_length = ecal.material.path_length(ptc)
        self.propagator(ptc).propagate_one(ptc,
                                           ecal.volume.inner,
                                           self.detector.elements['field'].magnitude)
        time_ecal_inner = ptc.path.time_at_z(ptc.points['ecal_in'].Z())
        deltat = ptc.path.deltat(path_length)
        time_decay = time_ecal_inner + deltat
        point_decay = ptc.path.point_at_time(time_decay)
        ptc.points['ecal_decay'] = point_decay
        frac_ecal = 0.
        if ecal.volume.contains(point_decay):
            frac_ecal = random.uniform(0., 0.7)
            self.make_cluster(ptc, 'ecal', frac_ecal)
        self.make_cluster(ptc, 'hcal', 1-frac_ecal)

    def reconstruct_charged_hadron(self, ptc):
        # create reconstructed ECAL and HCAL deposits
        # possibly smear position ECAL and HCAL
        # smear total energy        
        pass
    
    def simulate(self, ptcs):
        self.reset()
        self.ptcs = ptcs
        for ptc in ptcs:
            if ptc.pdgid == 22:
                self.simulate_photon(ptc)
            elif abs(ptc.pdgid) == 11:
                self.simulate_electron(ptc)
            elif abs(ptc.pdgid) == 13:
                self.simulate_muon(ptc)
            elif abs(ptc.pdgid) > 100: #TODO make sure this is ok
                self.simulate_hadron(ptc)
            
                
if __name__ == '__main__':

    import math
    from heppy_fcc.fastsim.vectors import Point
    from heppy_fcc.fastsim.detectors.CMS import CMS
    from heppy_fcc.fastsim.toyevents import particles
    from heppy_fcc.display.core import Display
    from heppy_fcc.display.geometry import GDetector
    from heppy_fcc.display.pfobjects import GTrajectories

    cms = CMS()
    simulator = Simulator(cms)
    particles = list(particles(1, 130, 1, 2,
                               5., 5.) )
    simulator.simulate(particles)

    display = Display(['xy', 'ECAL_thetaphi', 'HCAL_thetaphi'])
    gcms = GDetector(cms)
    display.register(gcms, 0)
    gtrajectories = GTrajectories(particles)
    display.register(gtrajectories,1)
    display.draw()
