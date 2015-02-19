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

    def propagate(self, ptc):
        is_neutral = abs(ptc.charge)<0.5
        prop = self.prop_straight if is_neutral else self.prop_helix
        prop.propagate([ptc], self.detector.cylinders() )

    def simulate_photon(self, ptc):
        # true deposit:
        # straight extrapolation to ECAL
        # EM deposit all energy
        ecal = self.detector.elements['ecal']
        self.prop_straight.propagate_one(ptc,
                                         ecal.volume.inner)
        cluster_size = ecal.cluster_size(ptc)
        cylname = ecal.volume.inner.name
        ptc.clusters[cylname] = Cluster(ptc.p4.E(),
                                        ptc.points[cylname],
                                        cluster_size,
                                        cylname)

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
                                      ecal.volume.inner)
        cluster_size = ecal.cluster_size(ptc)
        cylname = ecal.volume.inner.name
        ptc.clusters[cylname] = Cluster(ptc.p4.E(),
                                        ptc.points[cylname],
                                        cluster_size,
                                        cylname)

    def reconstruct_electron(self, ptc):
        # create reconstructed EM deposit
        # possibly smear position EM
        # smear energy EM        
        pass

    def make_cluster(self, ptc, detname, fraction=1., size=None):
        detector = self.detector.elements[detname]
        propagator = self.prop_helix if ptc.charge!=0 else self.prop_straight
        propagator.propagate_one(ptc,
                                 detector.volume.inner)
        if size is None:
            size = detector.cluster_size(ptc)
        cylname = detector.volume.inner.name
        ptc.clusters[cylname] = Cluster(ptc.p4.E()*fraction,
                                             ptc.points[cylname],
                                             size,
                                             cylname)
        
    
    def simulate_charged_hadron(self, ptc):
        # helix extrap to ECAL
        # estimate crossed ECAL material (straight extrap)
        # shower probability
        # if shower,
        #    decide on ECAL fraction
        #    straight extrap to HCAL
        #    HCAL deposit = (1-fecal)*E
        # else
        #    helix extrap to HCAL
        #    HCAL deposit = E
        frac_ecal = random.uniform(0., 1.)
        # TODO really dirty! need some kind of detector definition
        self.make_cluster(ptc, 'ecal', frac_ecal)
        self.make_cluster(ptc, 'hcal', 1-frac_ecal)
        print frac_ecal, 1-frac_ecal

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
                self.simulate_charged_hadron(ptc)
            
                
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
    particles = list(particles(5, 211, math.pi/3., 2*math.pi/3.,
                               10., 10.) )
    simulator.simulate(particles)

    display = Display()
    gcms = GDetector(cms)
    display.register(gcms, 0)
    gtrajectories = GTrajectories(particles)
    display.register(gtrajectories,1)
    display.draw()
