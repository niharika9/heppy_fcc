from heppy.utils.deltar import deltaR

class Distance(object):
    '''Concrete distance calculator.
    ''' 
    def __call__(self, ele1, ele2):
        '''returns a tuple: 
          True/False depending on the validity of the link
          float      the link distance
        '''
        layer1, layer2 = ele1.layer, ele2.layer
        if layer2 < layer1:
            layer1, layer2 = layer2, layer1
            ele1, ele2 = ele2, ele1
        layers = layer1, layer2
        func = None
        if layers == ('ecal_in', 'tracker'):
            func = self.ecal_track
        elif layers == ('hcal_in', 'tracker'):
            func = self.hcal_track
        elif layers == ('ecal_in', 'hcal_in'):
            func = self.ecal_hcal
        elif layers == ('ecal_in', 'ecal_in'):
            func = self.ecal_ecal
        elif layers == ('hcal_in', 'hcal_in'):
            func = self.hcal_hcal
        elif layers == ('tracker', 'tracker'):
            func = self.no_link
        else:
            raise ValueError('no such link layer:', layers)
        return func(ele1, ele2)        

    def no_link(self, ele1, ele2):
        return None, False, None
    
    def ecal_ecal(self, ele1, ele2):
        dR = deltaR(ele1.position.Eta(),
                    ele1.position.Phi(),
                    ele2.position.Eta(),
                    ele2.position.Phi())
        link_ok = dR < ele1.size + ele2.size
        return ('ecal_in', 'ecal_in'), link_ok, dR 

    def hcal_hcal(self, ele1, ele2):
        dR = deltaR(ele1.position.Eta(),
                    ele1.position.Phi(),
                    ele2.position.Eta(),
                    ele2.position.Phi())
        link_ok = dR < ele1.size + ele2.size
        return ('hcal_in', 'hcal_in'), link_ok, dR 
    
    def ecal_track(self, ecal, track):
        tp = track.path.points['ecal_in']
        cp = ecal.position
        dR = deltaR(tp.Eta(),
                    tp.Phi(),
                    cp.Eta(),
                    cp.Phi())
        link_ok = dR < ecal.size 
        return ('ecal_in', 'tracker'), link_ok, dR 
        
    def hcal_track(self, hcal, track):
        tp = track.path.points['hcal_in']
        cp = hcal.position
        dR = deltaR(tp.Eta(),
                    tp.Phi(),
                    cp.Eta(),
                    cp.Phi())
        link_ok = dR < hcal.size
        return ('hcal_in', 'tracker'), link_ok, dR

    def ecal_hcal(self, ele1, ele2):
        #TODO eta or theta? 
        dR = deltaR(ele1.position.Eta(),
                    ele1.position.Phi(),
                    ele2.position.Eta(),
                    ele2.position.Phi())
        link_ok = dR < ele1.size + ele2.size
        return ('ecal_in', 'hcal_in'), link_ok, dR 

distance = Distance()
