from heppy.utils.deltar import deltaR

class Distance(object):
    '''Concrete distance calculator.
    ''' 
    def __call__(self, ele1, ele2):
        '''returns a tuple: 
          True/False depending on the validity of the link
          float      the link distance
        ''' 
        layer1 = ele1.layer
        layer2 = ele2.layer
        if layer1 == layer2:
            return None, False, None
        layers = tuple(sorted([layer1, layer2]))
        func = None
        if layers == ('ecal_in', 'tracker'):
            func = self.ecal_track
        elif layers == ('hcal_in', 'tracker'):
            func = self.hcal_track
        elif layers == ('ecal_in', 'hcal_in'):
            func = self.ecal_hcal
        else:
            raise ValueError('no such link layer:', layers)
        return func(ele1, ele2)
        
    def ecal_track(self, ele1, ele2):
        return ('ecal_in', 'tracker'), True, 1. 

    def hcal_track(self, ele1, ele2):
        return ('hcal_in', 'tracker'), True, 1. 

    def ecal_hcal(self, ele1, ele2):
        #TODO eta or theta? 
        dR = deltaR(ele1.position.Eta(),
                    ele1.position.Phi(),
                    ele2.position.Eta(),
                    ele2.position.Phi())
        link_ok = dR < ele1.size + ele2.size
        return ('ecal_in', 'hcal_in'), link_ok, dR 

distance = Distance()
