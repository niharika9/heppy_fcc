import math

class JetComponent(list):

    def __init__(self):
        super(JetComponent, self).__init__()
        self._e = 0
        self._pt = 0
        self._num = 0
        self._pdgid = None

    def pdgid(self):
        return self._pdgid
        
    def e(self):
        return self._e

    def pt(self):
        return self._pt

    def num(self):
        return self._num
    
    def append(self, ptc):
        if self._pdgid is None:
            self._pdgid = ptc.pdgid()
        elif ptc.pdgid()!=self._pdgid:
            raise ValueError('cannot add particles of different type to a component')
        super(JetComponent, self).append(ptc)
        self._e += ptc.e()
        self._pt += ptc.pt()
        self._num += 1

    def __str__(self):
        header = 'pdgid={pdgid}, n={num:d}, e={e:3.1f}, pt={pt:3.1f}'.format(
            pdgid = self.pdgid(),
            num = self.num(),
            e = self.e(),
            pt = self.pt()
        )
        ptcs = []
        for ptc in self:
            ptcs.append('\t{particle}'.format(particle=str(ptc)))
        result = [header]
        result.extend(ptcs)
        return '\n'.join(result)
        

class JetConstituents(object):

    def __init__(self):
        self.components = dict()

    def append(self, ptc):
        self.components.setdefault(ptc.pdgid(), JetComponent()).append(ptc)

    def sort(self):
        for ptcs in self.components.values():
            ptcs.sort(key = lambda ptc: ptc.e(), reverse=True)

            
class Jet(object):
    
    def p4(self):
        return self.tlv

    def p3(self):
        return self.tlv.Vect()
    
    def e(self):
        return self.tlv.E()

    def pt(self):
        return self.tlv.Pt()
    
    def theta(self):
        return math.pi/2 - self.tlv.Theta()

    def eta(self):
        return self.tlv.Eta()

    def phi(self):
        return self.tlv.Phi()

    def m(self):
        return self.tlv.M()

    def __str__(self):
        tmp = '{className} : e = {e:5.1f}, theta = {theta:5.2f}, phi = {phi:5.2f}, mass = {m:5.2f}'
        return tmp.format(
            className = self.__class__.__name__,
            e = self.e(),
            theta = self.theta(),
            phi = self.phi(),
            m = self.m()
            )
    
