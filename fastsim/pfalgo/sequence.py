from pfinput import PFInput
from links import Links
from distance import distance
from pfreconstructor import PFReconstructor

#TODO: this class and PFInput should probably be in the fastsim module, to try to keep the pfalgo package independent from the dataformat in use. 

class PFSequence(object):
    
    def __init__(self, simptcs):
        self.recptcs = self.reconstruct(simptcs)

    def reconstruct(self, simptcs):
        self.pfinput = PFInput(simptcs)
        elements = self.pfinput.element_list()
        self.links = Links(elements, distance)
        print self.pfinput
        print self.links
        self.pfreco = PFReconstructor( self.links.groups() )
        print self.pfreco

