from detector import Detector, DetectorElement
import material
from geometry import VolumeCylinder
import math

class ECAL(DetectorElement):

    def __init__(self):
        volume = VolumeCylinder('ecal', 1.55, 2.25, 1.30, 2. )
        mat = material.Material('ECAL', 8.9e-3, 0.25)
        super(ECAL, self).__init__('ecal', volume,  mat)

    def energy_resolution(self, ptc):
        E = ptc.p4.E()
        return 0.07 / math.sqrt(E) + 0.001

    def cluster_size(self, ptc):
        pdgid = abs(ptc.pdgid)
        if pdgid==22 or pdgid==11:
            return 0.05
        else:
            return 0.07

    def space_resolution(self, ptc):
        pass

    
class HCAL(DetectorElement):

    def __init__(self):
        volume = VolumeCylinder('hcal', 2.9, 3.6, 1.9, 2.6 )
        mat = material.Material('HCAL', None, 0.17)
        super(HCAL, self).__init__('ecal', volume, mat)

    def energy_resolution(self, ptc):
        E = ptc.p4.E()
        return 1.1/ math.sqrt(E) 

    def cluster_size(self, ptc):
        return 0.2

    def space_resolution(self, ptc):
        pass


class Tracker(DetectorElement):
    
    def __init__(self):
        volume = VolumeCylinder('tracker', 1.29, 1.99)
        mat = material.void
        super(Tracker, self).__init__('tracker', volume,  mat)

        
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
