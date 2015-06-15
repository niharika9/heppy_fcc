from heppy.framework.analyzer import Analyzer
from heppy.utils.deltar import matchObjectCollection, deltaR

class Matcher(Analyzer):

    def process(self, event):
        particles = getattr(event, self.cfg_ana.particles)
        match_particles = getattr(event, self.cfg_ana.match_particles)
        pairs = matchObjectCollection(particles, match_particles, 0.3**2)
        for ptc in particles:
            ptc.match = pairs[ptc]
            if ptc.match:
                ptc.dR = deltaR(ptc.theta(), ptc.phi(),
                                ptc.match.theta(), ptc.match.phi())
                # print ptc.dR, ptc, ptc.match
