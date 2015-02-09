import copy

#TODO propagator (separate module)

class SurfaceCylinder(object):
    def __init__(self, name, rad, z):
        self.name = name
        self.rad = rad
        self.z = z
   
class VolumeCylinder(object):
    '''Implement sub even for pipes, and consistency test: all space must be filled.'''
    
    def __init__(self, name, outer, inner=None):
        if not isinstance(name, basestring):
            raise ValueError('first parameter must be a string')
        self.name = name
        self.outer = outer
        self.inner = inner
        if inner is not None: 
            if inner.rad > outer.rad:
                raise ValueError('outer radius of subtracted cylinder must be smaller')
            if inner.z > outer.z :
                raise ValueError('outer z of subtracted cylinder must be smaller')
 
    
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
        otracker = SurfaceCylinder('tracker', 1.3, 2.)
        oecal = SurfaceCylinder('oecal', 1.8, 2.4)
        ohcal = SurfaceCylinder('ohcal', 2.9, 3.5)
        tracker = VolumeCylinder('tracker', otracker )
        ecal = VolumeCylinder( 'ecal', oecal, tracker.outer )
        hcal = VolumeCylinder( 'hcal', ohcal, ecal.outer )
        field = 3.8
        self.elements['tracker'] = DetectorElement('tracker', tracker, material_void, field)
        self.elements['ecal'] = DetectorElement('ecal', ecal, material_CMS_ECAL, field)
        self.elements['hcal'] = DetectorElement('hcal', hcal, material_CMS_HCAL, field)



        
