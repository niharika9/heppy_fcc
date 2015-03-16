from heppy.utils.deltar import deltaR

class Distance(object):
    '''Concrete distance calculator.
    ''' 
    def __call__(self, ele1, ele2):
        '''returns a tuple: 
          True/False depending on the validity of the link
          float      the link distance
        ''' 
        type1 = ele1.type
        type2 = ele2.type
        if type1 == type2:
            return None, False, None
        types = tuple(sorted([type1, type2]))
        func = None
        if types == ('ecal', 'track'):
            func = self.ecal_track
        elif types == ('hcal', 'track'):
            func = self.hcal_track
        elif types == ('ecal', 'hcal'):
            func = self.ecal_hcal
        else:
            raise ValueError('no such link type:', types)
        return func(ele1, ele2)
        
    def ecal_track(self, ele1, ele2):
        return ('ecal', 'track'), True, 1. 

    def hcal_track(self, ele1, ele2):
        return ('hcal', 'track'), True, 1. 

    def ecal_hcal(self, ele1, ele2):
        #TODO eta or theta? 
        dR = deltaR(ele1.position.Eta(),
                    ele1.position.Phi(),
                    ele2.position.Eta(),
                    ele2.position.Phi())
        link_ok = dR < ele1.size + ele2.size
        return ('ecal', 'hcal'), link_ok, dR 
        
