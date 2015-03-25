from pfinput import PFInput
from links import Links
from distance import distance
from pfreconstructor import PFReconstructor

#TODO: this class and PFInput should probably be in the fastsim module, to try to keep the pfalgo package independent from the dataformat in use. 

class PFSequence(object):
    
    def __init__(self, simptcs, detector):
        self.recptcs = self.reconstruct(simptcs, detector)

    def reconstruct(self, simptcs, detector):
        self.pfinput = PFInput(simptcs)
        elements = self.pfinput.element_list()
        self.links = Links(elements, distance)
        print self.pfinput
        print self.links
        self.pfreco = PFReconstructor( self.links, detector )
        print self.pfreco
        print self.links
