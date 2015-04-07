from vectors import Point
from heppy.utils.deltar import deltaR
import math

class PFObject(object):

    def __init__(self):
        self.linked = []
        self.locked = False
        self.block_label = None

    def accept(self, visitor):
        '''Called by visitors, such as FloodFill.'''
        notseen = visitor.visit(self)
        if notseen:
            for elem in self.linked:
                elem.accept(visitor)

    def __repr__(self):
        return str(self)


class Cluster(PFObject):

    #TODO: not sure this plays well with SmearedClusters
    max_energy = 0.
    
    def __init__(self, energy, position, size_m, layer, particle=None):
        super(Cluster, self).__init__()
        self.position = position
        self.set_energy(energy)
        self.set_size(size_m)
        self.layer = layer
        self.particle = particle
        # self.absorbed = []

    def set_size(self, value):
        self._size = value
        try:
            self._angularsize = math.atan( self._size / self.position.Mag() ) 
        except:
            import pdb; pdb.set_trace()
            
    def size(self):
        return self._size

    def angular_size(self):
        return self._angularsize

    def is_inside(self, point):
        dist = (self.position - point).Mag()
        if dist < self.size():
            return True, dist
        else:
            return False, dist
        
    # def absorb(self, other):
    #     subs = list(self.absorbed)
    #     subs.append(self)
    #     osubs = list(other.absorbed)
    #     osubs.append(other)
    #     for sub in subs:
    #         for osub in osubs:
    #             if deltaR(sub.position.Eta(),
    #                       sub.position.Phi(),
    #                       osub.position.Eta(),
    #                       osub.position.Phi()) < sub.size + osub.size:
    #                 self.absorbed.extend(osubs)
    #                 self.set_energy( self.energy + other.energy ) 
    #                 return True
    #     return False
                    
    def set_energy(self, energy):
        self.energy = energy
        if energy > self.__class__.max_energy:
            self.__class__.max_energy = energy
        self.pt = energy * self.position.Unit().Perp()

    # fancy but I prefer the other solution
    # def __setattr__(self, name, value):
    #     if name == 'energy':
    #         self.pt = value * self.position.Unit().Perp()
    #     self.__dict__[name] = value

    def __str__(self):
        return '{classname:15}: {layer:10} {energy:7.2f} {theta:5.2f} {phi:5.2f}'.format(
            classname = self.__class__.__name__,
            layer = self.layer,
            energy = self.energy,
            theta = math.pi/2. - self.position.Theta(),
            phi = self.position.Phi()
        )
        
class SmearedCluster(Cluster):
    def __init__(self, mother, *args, **kwargs):
        self.mother = mother
        super(SmearedCluster, self).__init__(*args, **kwargs)

        
class Track(PFObject):

    def __init__(self, p3, charge, path, particle=None):
        super(Track, self).__init__()
        self.p3 = p3
        self.pt = p3.Perp()
        self.energy = p3.Mag()  #TODO clarify energy and momentum
        self.charge = charge
        self.path = path
        self.particle = particle
        self.layer = 'tracker'

    def __str__(self):
        return '{classname:15}: {e:7.2f} {pt:7.2f} {theta:5.2f} {phi:5.2f}'.format(
            classname = self.__class__.__name__,
            pt = self.pt,
            e = self.energy, 
            theta = math.pi/2. - self.p3.Theta(),
            phi = self.p3.Phi()
        )
        

        
class SmearedTrack(Track):

    def __init__(self, mother, *args, **kwargs):
        self.mother = mother
        self.path = mother.path
        super(SmearedTrack, self).__init__(*args, **kwargs)
    
        
class Particle(object):
    def __init__(self, p4, vertex, charge, pdgid=None):
        self.p4 = p4
        self.p3 = p4.Vect()
        self.vertex = vertex
        self.charge = charge
        self.pdgid = pdgid
        self.path = None
        self.clusters = dict()
        # TODO remove track datamembers from self.
        self.track = Track(self.p3, self.charge, self.path)
        self.clusters_smeared = dict()
        self.track_smeared = None  
        
    def __getattr__(self, name):
        if name=='points':
            if self.path is None:
                import pdb; pdb.set_trace()
            return self.path.points
        
    def is_em(self):
        kind = abs(self.pdgid)
        if kind==11 or kind==22:
            return True
        else:
            return False
        
    def set_path(self, path, option=None):
        if option == 'w' or self.path is None:
            self.path = path
            self.track = Track(self.p3, self.charge, self.path)
        
    def __str__(self):
        return '{classname}: {pdgid:5} {charge:2} {mass:8.3f} {energy:6.2f} {theta:5.2f} {phi:5.2f}'.format(
            classname = self.__class__.__name__,
            pdgid = self.pdgid,
            charge = self.charge,
            mass = abs(self.p4.M()),
            energy = self.p4.E(),
            theta = math.pi/2. - self.p4.Theta(),
            phi = self.p4.Phi()
        )

    def __repr__(self):
        return str(self)

    
if __name__ == '__main__':
    from ROOT import TVector3
    cluster = Cluster(10., TVector3(1,0,0), 1, 1)
    print cluster.pt
    cluster.set_energy(5.)
    print cluster.pt
    
