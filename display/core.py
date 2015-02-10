from ROOT import TCanvas, TH1, TH2F
import operator

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
        #TODO might need to keep track of views in objects
        
    def draw(self):
        self.canvas.cd()
        for obj, layer in sorted(self.registered.items(),
                                 key = operator.itemgetter(1)):
            obj.draw(self.projection)
        self.canvas.Update()
