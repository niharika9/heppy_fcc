import math

class Particle(object):
    '''Interface for particles. 
    Make sure your code satisfies this interface.
    Specializations in cms, fcc, and tlv packages
    '''
    def p4(self):
        '''4-momentum, px, py, pz, E'''
        return self._tlv

    def p3(self):
        '''3-momentum px, py, pz'''
        return self._tlv.Vect()

    def e(self):
        '''energy'''
        return self._tlv.E()

    def pt(self):
        '''transverse momentum (magnitude of p3 in transverse plane)'''
        return self._tlv.Pt()
    
    def theta(self):
        '''angle w/r to transverse plane'''
        return math.pi/2 - self._tlv.Theta()

    def eta(self):
        '''pseudo-rapidity (-ln(tan self._tlv.Theta()/2)).
        theta = 0 -> eta = +inf
        theta = pi/2 -> 0 
        theta = pi -> eta = -inf
        '''
        return self._tlv.Eta()

    def phi(self):
        '''azymuthal angle (from x axis, in the transverse plane)'''
        return self._tlv.Phi()

    def m(self):
        '''mass'''
        return self._tlv.M()

    def pdgid(self):
        '''particle type'''
        return self._pid

    def q(self):
        '''particle charge'''
        return self._charge

    def status(self):
        '''status code, e.g. from generator. 1:stable.'''
        return self._status

    def start_vertex(self):
        '''start vertex (3d point)'''
        return self._start_vertex 

    def end_vertex(self):
        '''end vertex (3d point)'''
        return self._end_vertex

    def __str__(self):
        tmp = '{className} : pdgid = {pdgid:5}, status = {status:3}, q = {q:2} e = {e:5.1f}, eta = {eta:5.2f}, theta = {theta:5.2f}, phi = {phi:5.2f}, mass = {m:5.2f}'
        return tmp.format(
            className = self.__class__.__name__,
            pdgid = self.pdgid(),
            status = self.status(),
            q = self.q(),
            e = self.e(),
            eta = self.eta(),
            theta = self.theta(),
            phi = self.phi(),
            m = self.m()
            )
    
