import itertools


class Element(object):
    '''Basic interface for a particle flow element.
    Your class should expose the same attributes
    '''
    def __init__(self, layer):
        self.layer = layer
        self.linked = []


class Distance(object):
    '''Basic distance functor interface.
    You should provide such a functor (or a function), able to deal 
    with any pair of elements you have.
    ''' 
    def __call__(self, ele1, ele2):
        '''Should return True if the link is valid, 
        together with a link property object (maybe only the link distance).
        ''' 
        dist12 = 0.
        return True, dist12
        
        
class Link(object):
    def __init__(self, ele1, ele2, properties):
        self.ele1 = ele1
        self.ele2 = ele2
        self.properties = properties

        
class Linker(object):

    def __init__(self, elements, distance):
        '''
        parameters: 
          elements: list of Elements
          distance: function able to quantify the link between two elements
        '''
        self.distance = distance
        self.links = self.link(elements)

    def link(self, elements):
        links = dict()
        for ele1, ele2 in itertools.combinations(elements, 2):
            linked, dist = self.distance(ele1, ele2)
            if linked: 
                links[ele1, ele2] = dist
                ele1.linked.append(ele2)
                ele2.linked.append(ele1)
        return links

