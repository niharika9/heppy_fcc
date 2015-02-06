from ROOT import TEllipse, TBox, TCanvas, TH2F

#TODO display the field
#TODO display trajectories (tracks, particles, charged or not)
#TODO display deposits

class ViewPane(object):
    #TODO a view needs to know which objects are drawn.
    #TODO layers
    def __init__(self, name, nx, xmin, xmax, ny, ymin, ymax):
        self.canvas = TCanvas(name, name, 800, 800)
        self.hist = TH2F(name, name, nx, xmin, xmax, ny, ymin, ymax)
        self.hist.Draw()
        self.hist.SetStats(False)
        

        
class GDetectorElement(object):
    '''TODO improve design? 
    there could be one detector element per view, 
    and they would all be linked together. 
    '''
    def __init__(self, description):
        self.desc = description
        self.circles = []
        self.boxes = []
        self.circles.append( TEllipse(0., 0.,
                                      self.desc.volume.orad,
                                      self.desc.volume.orad) )
        dz = self.desc.volume.oz
        radius = self.desc.volume.orad
        self.boxes.append( TBox(-dz, -radius, dz, radius) ) 
        
        if self.desc.volume.irad>0. :
            self.circles.append( TEllipse(0., 0.,
                                          self.desc.volume.irad,
                                          self.desc.volume.irad))
            dz = self.desc.volume.iz
            radius = self.desc.volume.irad
            self.boxes.append( TBox(-dz, -radius, dz, radius) ) 
            
        color = self.desc.material.color
        if color:
            oc = self.circles[0]
            ob = self.boxes[0]
            for shape in [oc, ob]:
                shape.SetFillColor(self.desc.material.color)
                shape.SetFillStyle(1001)
            if len(self.circles)==2:
                ic = self.circles[1]
                ib = self.boxes[1]
                for shape in [ic, ib]:
                    shape.SetFillColor(0)
                    shape.SetFillStyle(1001)
            
    def draw_rhophi(self, *args):
        for circle in self.circles:
            circle.Draw(*args)

    def draw_rhoz(self, *args):
        for box in self.boxes:
            box.Draw(*args)


class GDetector(object):
    def __init__(self, description):
        self.desc = description
        self.elements = [GDetectorElement(elem) for elem in self.desc.elements.values()]
            
    def draw_rhophi(self, *args):
        for elem in self.elements:
            elem.draw_rhophi(*args)

    def draw_rhoz(self, *args):
        for elem in self.elements:
            elem.draw_rhoz(*args)

            
if __name__ == '__main__':

    from ROOT import TCanvas, TH2F
    from heppy_fcc.fastsim.geometry import CMS

    cms = CMS()
    gcms = GDetector(cms)

    #TODO need some kind of master display object
    rhophi = ViewPane("rhophi", 100, -5, 5, 100, -5, 5)
    gcms.draw_rhophi("same")
    rhoz = ViewPane("rhoz", 100, -5, 5, 100, -5, 5)
    gcms.draw_rhoz("same")
