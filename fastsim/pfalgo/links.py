import itertools
from floodfill import FloodFill

class Element(object):
    '''Basic interface for a particle flow element.
    Your class should expose the same attributes
    '''
    def __init__(self):
        self.layer = None
        self.linked = []
        self.locked = False
        self.block_label = None

    def accept(self, visitor):
        '''Called by visitors, such as FloodFill.'''
        notseen = visitor.visit(self)
        if notseen:
            for elem in self.linked:
                elem.accept(visitor)

                
class Distance(object):
    '''Basic distance functor interface.
    You should provide such a functor (or a function), able to deal 
    with any pair of elements you have.
    ''' 
    def __call__(self, ele1, ele2):
        '''Should return True if the link is valid, 
        together with a link property object (maybe only the link distance).
        '''
        link_type = 'dummy'
        dist12 = 0.
        return link_type, True, dist12
    
    
    
class Links(dict):

    def __init__(self, elements, distance):
        for ele1, ele2 in itertools.combinations(elements, 2):
            link_type, link_ok, dist = distance(ele1, ele2)
            if link_ok: 
                self.add(ele1, ele2, dist)
        self.floodfill = FloodFill(elements)
            
    def key(self, elem1, elem2):
        return tuple(sorted([elem1, elem2]))
    
    def add(self, elem1, elem2, link_info):
        key = self.key(elem1, elem2)
        elem1.linked.append(elem2)
        elem2.linked.append(elem1)
        self[key] = link_info

    def info(self, elem1, elem2):
        key = self.key(elem1, elem2)
        return self.get(key, None)

    def groups(self):
        return self.floodfill.groups
    
    def __str__(self):
        lines = []
        for key, val in self.iteritems():
            ele1, ele2 = key
            lines.append("{ele1:50} {ele2:50} {val:5.4f}".format(ele1=ele1,
                                                                 ele2=ele2,
                                                                 val=val))
        return '\n'.join(lines)



