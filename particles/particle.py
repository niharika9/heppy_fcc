import math

class Particle(object):
    
    def p4(self):
        return self.tlv

    def p3(self):
        return self.tlv.Vect()

    def e(self):
        return self.tlv.E()

    def theta(self):
        return math.pi/2 - self.tlv.Theta()

    def phi(self):
        return self.tlv.Phi()

    def m(self):
        return self.tlv.M()

    def pdgid(self):
        return self.pid

    def q(self):
        return self.charge
        
    def __str__(self):
        tmp = '{className} : pdgid = {pdgid:3} q = {q:1} e = {e:5.1f}, theta = {theta:5.2f}, phi = {phi:5.2f}, mass = {m:5.2f}'
        return tmp.format(
            className = self.__class__.__name__,
            pdgid = self.pdgid(),
            q = self.q(),
            e = self.e(),
            theta = self.theta(),
            phi = self.phi(),
            m = self.m()
            )
    
