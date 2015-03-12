import itertools


class Link(object):
    def __init__(self, ele1, ele2, properties):
        self.ele1 = ele1
        self.ele2 = ele2
        self.properties = properties

class Element(int):
    def __init__(self, val):
        self.linked = []
        super(Element, self).__init__(val)

class Linker(object):

    def __init__(self, elements, distance):
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
