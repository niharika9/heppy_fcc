from detector import Detector, DetectorElement
import material
from geometry import VolumeCylinder
import math

class ECAL(DetectorElement):

    def __init__(self):
        volume = VolumeCylinder('ecal', 1.55, 2.25, 1.30, 2. )
        mat = material.Material('ECAL', 8.9e-3, 0.25)
        super(ECAL, self).__init__('ecal', volume,  mat)

    def energy_resolution(self, cluster):
        E = cluster.energy
        return 0.07 / cluster.energy + 0.001

    def cluster_size(self, ptc):
        pdgid = abs(ptc.pdgid)
        if pdgid==22 or pdgid==11:
            return 0.04
        else:
            return 0.07

    def acceptance(self, cluster):
        energy = cluster.energy
        eta = abs(cluster.position.Eta())
        if eta < 1.5:
            return energy>2.
        elif eta < 3.:
            return cluster.pt>0.5
        else:
            return False

    def space_resolution(self, ptc):
        pass

    
class HCAL(DetectorElement):

    def __init__(self):
        volume = VolumeCylinder('hcal', 2.9, 3.6, 1.9, 2.6 )
        mat = material.Material('HCAL', None, 0.17)
        super(HCAL, self).__init__('ecal', volume, mat)

    def energy_resolution(self, cluster):
        return 1.1/ math.sqrt( cluster.energy ) 

    def cluster_size(self, ptc):
        return 0.2

    def acceptance(self, cluster):
        energy = cluster.energy
        eta = abs(cluster.position.Eta())
        if eta < 3. : 
            return energy>5.
        elif eta < 5.:
            return energy>10.
        else:
            return False
    
    def space_resolution(self, ptc):
        pass


class Tracker(DetectorElement):
    
    def __init__(self):
        volume = VolumeCylinder('tracker', 1.29, 1.99)
        mat = material.void
        super(Tracker, self).__init__('tracker', volume,  mat)

    def acceptance(self, ptc):
        pt = ptc.p4.Pt()
        eta = abs(ptc.p4.Eta())
        if eta < 2.5 : 
            return pt>0.7
        else:
            return False

    def pt_resolution(self, ptc):
        return 0.01
    

class Field(DetectorElement):

    def __init__(self, magnitude):
        self.magnitude = magnitude
        volume = VolumeCylinder('field', 2.9, 3.6)
        mat = material.void
        super(Field, self).__init__('tracker', volume,  mat)
        
        
class CMS(Detector):
    def __init__(self):
        super(CMS, self).__init__()
        self.elements['tracker'] = Tracker()
        self.elements['ecal'] = ECAL()
        self.elements['hcal'] = HCAL()
        self.elements['field'] = Field(3.8)


if __name__ == '__main__':

    cms = CMS()
