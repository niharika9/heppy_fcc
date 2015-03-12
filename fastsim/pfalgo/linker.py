import itertools


class Link(object):
    def __init__(self, ele1, ele2, prop):
        self.ele1 = ele1
        self.ele2 = ele2
        self.properties = properties


class Linker(object):
    def __init__(self, elements):
        self.links = self.link(elements)

    def link(self, elements):
        for ele1, ele2 in itertools.combinations(2, elements) 
        
