import operator

from ROOT import TEllipse, TBox, TCanvas, TH2F, TH1
from ROOT import TColor, kRed, kBlue

#TODO display the field
#TODO display trajectories (tracks, particles, charged or not)
#TODO display deposits


COLORS = dict(
    CMS_ECAL = kRed-10,
    CMS_HCAL = kBlue-10,
    void = None
) 


class Display(object):
    
    def __init__(self):
        self.views = dict(
            rhophi = ViewPane("rhophi", "rhophi", 100, -5, 5, 100, -5, 5),
            rhoz = ViewPane("rhoz", "rhoz", 100, -5, 5, 100, -5, 5)
            )

    def register(self, obj, layer):
        for view in self.views.values():
            view.register(obj, layer)
        
    def draw(self):
        for view in self.views.values():
            view.draw()
        

class ViewPane(object):
    #TODO a view needs to know which objects are drawn.
    #TODO layers
    def __init__(self, name, projection, nx, xmin, xmax, ny, ymin, ymax):
        self.projection = projection
        self.canvas = TCanvas(name, name, 800, 800)
        TH1.AddDirectory(False)
        self.hist = TH2F(name, name, nx, xmin, xmax, ny, ymin, ymax)
        TH1.AddDirectory(True)
        self.hist.Draw()
        self.hist.SetStats(False)
        self.registered = dict()
       
    def register(self, obj, layer):
        self.registered[obj] = layer
        
    def draw(self):
        self.canvas.cd()
        for obj, layer in sorted(self.registered.items(),
                                 key = operator.itemgetter(1)):
            obj.draw(self.projection)
        self.canvas.Update()

        
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
                                      self.desc.volume.outer.rad,
                                      self.desc.volume.outer.rad) )
        dz = self.desc.volume.outer.z
        radius = self.desc.volume.outer.rad
        self.boxes.append( TBox(-dz, -radius, dz, radius) ) 
        
        if self.desc.volume.inner:
            self.circles.append( TEllipse(0., 0.,
                                          self.desc.volume.inner.rad,
                                          self.desc.volume.inner.rad))
            dz = self.desc.volume.inner.z
            radius = self.desc.volume.inner.rad
            self.boxes.append( TBox(-dz, -radius, dz, radius) ) 
            
        color = COLORS[self.desc.material.name]
        if color:
            oc = self.circles[0]
            ob = self.boxes[0]
            for shape in [oc, ob]:
                shape.SetFillColor(color)
                shape.SetFillStyle(1001)
                shape.SetLineColor(1)
                shape.SetLineStyle(1)                
            if len(self.circles)==2:
                ic = self.circles[1]
                ib = self.boxes[1]
                for shape in [ic, ib]:
                    shape.SetFillColor(0)
                    shape.SetFillStyle(1001)

    def draw(self, projection):
        if projection == 'rhophi':
            for circle in self.circles:
                circle.Draw('same')
        elif projection == 'rhoz':
            for box in self.boxes:
                box.Draw('samel')
        else:
            raise ValueError('implement drawing for projection ' + projection )


class GDetector(object):
    def __init__(self, description):
        self.desc = description
        self.elements = [GDetectorElement(elem) for elem in self.desc.elements.values()]
            
    def draw(self, projection):
        for elem in self.elements:
            elem.draw(projection)


            
if __name__ == '__main__':

    from ROOT import TCanvas, TH2F
    from heppy_fcc.fastsim.geometry import CMS

    cms = CMS()
    gcms = GDetector(cms)

    display = Display()
    display.register(gcms, 0)
    display.draw()
