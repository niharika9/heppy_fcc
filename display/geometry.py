from ROOT import TEllipse, TCanvas, TH2F

class ViewPane(object):
    def __init__(self, name, nx, xmin, xmax, ny, ymin, ymax):
        self.canvas = TCanvas(name, name, 800, 800)
        self.hist = TH2F(name, name, nx, xmin, xmax, ny, ymin, ymax)
        self.hist.Draw()

        
class GDetectorElement(object):
    def __init__(self, description):
        self.desc = description
        self.circles = []
        self.circles.append( TEllipse(0., 0.,
                                      self.desc.volume.orad,
                                      self.desc.volume.orad) )
        if self.desc.volume.irad>0. :
            self.circles.append( TEllipse(0., 0.,
                                          self.desc.volume.irad,
                                          self.desc.volume.irad))

    def draw_rhophi(self, *args):
        for circle in self.circles:
            circle.Draw(*args)


class GDetector(object):
    def __init__(self, description):
        self.desc = description
        self.elements = [GDetectorElement(elem) for elem in self.desc.elements.values()]
            
    def draw_rhophi(self, *args):
        for elem in self.elements:
            elem.draw_rhophi(*args)
            
            
if __name__ == '__main__':

    from ROOT import TCanvas, TH2F
    from heppy_fcc.fastsim.geometry import CMS

    rhophi = ViewPane("rhophi", 100, -5, 5, 100, -5, 5)
    cms = CMS()
    gcms = GDetector(cms)
    gcms.draw_rhophi("same")
    
