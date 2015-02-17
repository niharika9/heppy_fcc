from heppy_fcc.fastsim.propagator import StraightLinePropagator, HelixPropagator 


class Simulator(object):

    def __init__(self, detector):
        self.detector = detector
        self.prop_helix = HelixPropagator()
        self.prop_straight = StraightLinePropagator()
        
    def reset(self):
        self.particles = None
        
    def simulate(self, particles):
        self.reset()
        self.particles = particles 
        for ptc in particles:
            is_neutral = abs(ptc.charge)<0.5
            prop = self.prop_straight if is_neutral else self.prop_helix
            prop.propagate([ptc], self.detector.cylinders() )
 
if __name__ == '__main__':

    import math
    from heppy_fcc.fastsim.vectors import Point
    from heppy_fcc.fastsim.geometry import CMS
    from heppy_fcc.fastsim.toyevents import particles

    cms = CMS()
    simulator = Simulator(cms)
    particles = particles(5, 1, 0.5, math.pi/5., 4*math.pi/5.,
                          10., 10., Point(0.5,0.5,0))
    simulator.simulate(particles)
