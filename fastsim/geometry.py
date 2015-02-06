import copy


class Cylinder(object):
    '''Implement sub even for pipes, and consistency test: all space must be filled.'''
    
    def __init__(self, name, orad, oz, irad=0., iz=0.):
        self.name = name
        self.irad = irad
        self.orad = orad
        self.iz = iz
        self.oz = oz

    def __sub__(self, other):
        if other.irad > 1e-9 or other.iz > 1e-9:
            raise ValueError('inner radius and z of subtracted cylinder must be 0.')
        if other.orad > self.orad:
            raise ValueError('outer radius of subtracted cylinder must be smaller')
        if other.oz > self.oz :
            raise ValueError('outer z of subtracted cylinder must be smaller')
        orad = self.orad
        oz = self.oz
        irad = other.orad
        iz = other.oz
        return Cylinder('-'.join([self.name, other.name]),
                        orad, oz, irad, iz)
        
    
class Material(object):
    def __init__(self, name, x0, lambdaI):
        self.name = name
        self.x0 = x0
        self.lambdaI = lambdaI 

        
material_CMS_ECAL = Material('CMS_ECAL', 8.9e-3, 0.25)
material_CMS_HCAL = Material('CMS_HCAL', None, 0.17)
material_void = Material('void', 0., 0.)


class DetectorElement(object):
    def __init__(self, name, volume, material, field):
        self.name = name
        self.volume = volume
        self.material = material
        self.field = field

    
class Detector(object):
    def __init__(self):
        self.elements = dict()
        
        
        
class CMS(Detector):
    def __init__(self):
        super(CMS, self).__init__()
        tracker = Cylinder('tracker', 1.3, 2.)
        oecal = Cylinder('oecal', 1.8, 2.4)
        ohcal = Cylinder('ohcal', 2.9, 3.5)
        ecal = oecal - tracker
        hcal = ohcal - oecal
        field = 3.8
        self.elements['tracker'] = DetectorElement('tracker', tracker, material_void, field)
        self.elements['ecal'] = DetectorElement('ecal', ecal, material_CMS_ECAL, field)
        self.elements['hcal'] = DetectorElement('hcal', hcal, material_CMS_HCAL, field)



        
