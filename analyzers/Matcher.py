from heppy.framework.analyzer import Analyzer
from heppy.utils.deltar import matchObjectCollection, deltaR

import collections

class Matcher(Analyzer):

    def beginLoop(self, setup):
        super(Matcher, self).beginLoop(setup)
        self.match_collections = []
        if isinstance( self.cfg_ana.match_particles, basestring):
            self.match_collections.append( (self.cfg_ana.match_particles, None) )
        else:
            self.match_collections = self.cfg_ana.match_particles
        
    def process(self, event):
        particles = getattr(event, self.cfg_ana.particles)
        # match_particles = getattr(event, self.cfg_ana.match_particles)
        for collname, pdgid in self.match_collections:
            match_ptcs = getattr(event, collname)
            match_ptcs_filtered = match_ptcs
            if pdgid is not None:
                match_ptcs_filtered = [ptc for ptc in match_ptcs
                                       if ptc.pdgid()==pdgid]
            pairs = matchObjectCollection(particles, match_ptcs_filtered,
                                          0.3**2)
            for ptc in particles:
                matchname = 'match'
                if pdgid: 
                    matchname = 'match_{pdgid}'.format(pdgid=pdgid)
                match = pairs[ptc]
                setattr(ptc, matchname, match)
                if match:
                    drname = 'dr'
                    if pdgid:
                        drname = 'dr_{pdgid}'.format(pdgid=pdgid)
                    dr = deltaR(ptc.theta(), ptc.phi(),
                                match.theta(), match.phi())
                    setattr(ptc, drname, dr)
                    # print dr, ptc, match
