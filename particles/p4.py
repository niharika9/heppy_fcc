class P4(object):

    def pt(self):
        return self.read().Core.P4.Pt
    def eta(self):
        return self.read().Core.P4.Eta
    def phi(self):
        return self.read().Core.P4.Phi
    def mass(self):
        return self.read().Core.P4.Mass
    
    def __str__(self):
        tmp = '{className} : pt = {pt:5.1f}, eta = {eta:5.2f}, phi = {phi:5.2f}, mass = {mass:5.2f}'
        return tmp.format( className = self.__class__.__name__,
                           pt = self.pt(),
                           eta = self.eta(),
                           phi = self.phi(),
                           mass = self.mass() )
    
