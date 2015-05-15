import math

def group_pdgid(ptc):
    pdgid = abs(ptc.pdgid())
    if pdgid>100:
        if ptc.q():
            return 211
        else:
            return 130
    else:
        return pdgid

class JetComponent(list):

    def __init__(self, pdgid):
        super(JetComponent, self).__init__()
        self._e = 0
        self._pt = 0
        self._num = 0
        self._pdgid = pdgid

    def pdgid(self):
        return self._pdgid
        
    def e(self):
        return self._e

    def pt(self):
        return self._pt

    def num(self):
        return self._num
    
    def append(self, ptc):
        pdgid = group_pdgid(ptc)
        if self._pdgid is None:
            self._pdgid = pdgid
        elif pdgid!=self._pdgid:
            raise ValueError('cannot add particles of different type to a component')
        super(JetComponent, self).append(ptc)
        self._e += ptc.e()
        self._pt += ptc.pt()
        self._num += 1

    def __str__(self):
        header = '\t\tpdgid={pdgid}, n={num:d}, e={e:3.1f}, pt={pt:3.1f}'.format(
            pdgid = self.pdgid(),
            num = self.num(),
            e = self.e(),
            pt = self.pt()
        )
        ptcs = []
        for ptc in self:
            ptcs.append('\t\t\t{particle}'.format(particle=str(ptc)))
        result = [header]
        result.extend(ptcs)
        return '\n'.join(result)
        
 
class JetConstituents(dict):

    def __init__(self):
        super(JetConstituents, self).__init__()
        all_pdgids = [211, 22, 130, 11, 13]
        for pdgid in all_pdgids:
            self[pdgid] = JetComponent(pdgid)
    
    def append(self, ptc):
        pdgid = group_pdgid(ptc)
        # self.setdefault(pdgid, JetComponent(pdgid)).append(ptc)
        self[pdgid].append(ptc)
        
    def sort(self):
        for ptcs in self.values():
            ptcs.sort(key = lambda ptc: ptc.e(), reverse=True)

    def __str__(self):
        return '\n'.join(map(str, self.values()))
            
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
    
