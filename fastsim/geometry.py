import copy
import operator

#TODO propagator (separate module)
#TODO lock display elements (shouldn't be able to move them.)

class SurfaceCylinder(object):
    def __init__(self, name, rad, z):
        self.name = name
        self.rad = rad
        self.z = z
   
class VolumeCylinder(object):
    '''Implement sub even for pipes, and consistency test: all space must be filled.'''
    
    def __init__(self, name, orad, oz, irad=None, iz=None):
        if not isinstance(name, basestring):
            raise ValueError('first parameter must be a string')
        self.name = name
        self.outer = SurfaceCylinder('_'.join([self.name, 'out']), orad, oz)
        self.inner = None
        if irad and iz: 
            if irad > orad:
                raise ValueError('outer radius of subtracted cylinder must be smaller')
            if iz > oz :
                raise ValueError('outer z of subtracted cylinder must be smaller')
            if irad is None or iz is None:
                raise ValueError('must specify both irad and iz.')    
            self.inner = SurfaceCylinder('_'.join([self.name, 'in']), irad, iz)
    
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
    #TODO validate geometry consistency (no hole, no overlapping volumes)
    def __init__(self):
        self.elements = dict()
        self._cylinders = []
        
    def cylinders(self):
        if len(self._cylinders):
            return self._cylinders
        for element in self.elements.values():
            if element.volume.inner is not None: 
                self._cylinders.append(element.volume.inner)
            self._cylinders.append(element.volume.outer)
        self._cylinders.sort(key=operator.attrgetter("rad"))
        return self._cylinders
    
class CMS(Detector):
    def __init__(self):
        super(CMS, self).__init__()
        field = 3.8
        tracker = VolumeCylinder('tracker', 1.29, 1.99)
        ecal = VolumeCylinder('ecal', 1.89, 2.59, 1.30, 2. )
        hcal = VolumeCylinder('hcal', 2.9, 3.6, 1.9, 2.6 )
        self.elements['tracker'] = DetectorElement('tracker',
                                                   tracker,
                                                   material_void, field)
        self.elements['ecal'] = DetectorElement('ecal',
                                                ecal, material_CMS_ECAL, field)
        self.elements['hcal'] = DetectorElement('hcal',
                                                hcal, material_CMS_HCAL, field)



        
