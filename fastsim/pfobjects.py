from vectors import Point
import random


class Cluster(object):

    #TODO: not sure this plays well with SmearedClusters
    max_energy = 0.
    
    def __init__(self, energy, position, size, layer, particle=None):
        self.position = position
        self.set_energy(energy)
        self.size = size
        self.layer = layer
        self.particle = particle

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
        return '{classname}: {layer} {energy:5.2f} {theta:5.2f} {phi:5.2f}'.format(
            classname = self.__class__.__name__,
            layer = self.layer,
            energy = self.energy,
            theta = self.position.Theta(),
            phi = self.position.Phi()
        )

    def smear(self, detector, accept=False):
        '''Returns a copy of self with a smeared energy.  
        If accept is False (default), returns None if the smeared 
        cluster is not in the detector acceptance. '''
        #TODO I don't like to have this here. Should be in simulator
        eres = detector.energy_resolution(self)
        energy = self.energy * random.gauss(1, eres)
        smeared_cluster = SmearedCluster( self,
                                          energy,
                                          self.position,
                                          self.size,
                                          self.layer,
                                          self.particle )
        # smeared_cluster.set_energy(energy)
        if detector.acceptance(smeared_cluster) or accept:
            return smeared_cluster
        else:
            return None

        
class SmearedCluster(Cluster):
    def __init__(self, mother, *args, **kwargs):
        self.mother = mother
        super(SmearedCluster, self).__init__(*args, **kwargs)

        
class Track(object):

    def __init__(self, p3, charge, path, particle=None):
        self.p3 = p3
        self.pt = p3.Perp()
        self.charge = charge
        self.path = path
        self.particle = particle

    def smear(self, detector, accept=False):
        #TODO smearing depends on particle type!
        #TODO this is wierd. put this code in smeared track constructor
        # or in simulator
        ptres = detector.pt_resolution(self)
        scale_factor = random.gauss(1, ptres)
        smeared_track = SmearedTrack(self,
                                     self.p3 * scale_factor,
                                     self.charge,
                                     self.path)
        if detector.acceptance(smeared_track) or accept:
            return smeared_track
        else:
            return None
        
class SmearedTrack(Track):

    def __init__(self, mother, *args, **kwargs):
        self.mother = mother
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
        return '{classname}: {pdgid} {charge} {mass:5.2f} {energy:5.2f} {theta:5.2f} {phi:5.2f}'.format(
            classname = self.__class__.__name__,
            pdgid = self.pdgid,
            charge = self.charge,
            mass = abs(self.p4.M()),
            energy = self.p4.E(),
            theta = self.p4.Theta(),
            phi = self.p4.Phi()
        )
        
# class Track(Trajectory):
#     pass
    
if __name__ == '__main__':
    from ROOT import TVector3
    cluster = Cluster(10., TVector3(1,0,0), 1, 1)
    print cluster.pt
    cluster.set_energy(5.)
    print cluster.pt
    
