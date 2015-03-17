

class Element(basestring):
    def __init__(self, linked):
        self.linked = linked

        
class FloodFill(object):
    
    def __init__(self, elements):
        self.label = 0
        self.visited = dict()
        self.groups = dict()
        for elem in elements:
            if self.visited.get(elem, False):
                continue
            elem.accept(self)
            # print 'incrementing', elem, self.label
            self.label += 1

    def visit(self, element):
        if self.visited.get(element, False):
            return False
        else:
            # print 'visiting', element, self.label
            element.block_label = self.label
            self.groups.setdefault(element.block_label, []).append(element)
            self.visited[element] = True
            return True


