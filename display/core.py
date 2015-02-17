from ROOT import TCanvas, TH1, TH2F
import operator

class Display(object):
    
    def __init__(self):
        ViewPane.nviews = 0
        self.views = dict(
            xy = ViewPane("xy", "xy", 100, -5, 5, 100, -5, 5),
            yz = ViewPane("yz", "yz", 100, -5, 5, 100, -5, 5),
            xz = ViewPane("xz", "xz", 100, -5, 5, 100, -5, 5)
            )

    def register(self, obj, layer):
        elems = [obj]
        if hasattr(obj, '__iter__'):
            elems = obj
        for elem in elems: 
            for view in self.views.values():
                view.register(elem, layer)
            
    def draw(self):
        for view in self.views.values():
            view.draw()
        

class ViewPane(object):
    nviews = 0
    def __init__(self, name, projection, nx, xmin, xmax, ny, ymin, ymax):
        self.projection = projection
        dx = 600
        dy = 600
        tx = 50 + self.__class__.nviews * (dx+10) 
        ty = 50
        self.canvas = TCanvas(name, name, tx, ty, dx, dy)
        TH1.AddDirectory(False)
        self.hist = TH2F(name, name, nx, xmin, xmax, ny, ymin, ymax)
        TH1.AddDirectory(True)
        self.hist.Draw()
        self.hist.SetStats(False)
        self.registered = dict()
        self.__class__.nviews += 1 
        
    def register(self, obj, layer):
        self.registered[obj] = layer
        #TODO might need to keep track of views in objects
        
    def draw(self):
        self.canvas.cd()
        for obj, layer in sorted(self.registered.items(),
                                 key = operator.itemgetter(1)):
            obj.draw(self.projection)
        self.canvas.Update()

    def zoom(self, xmin, xmax, ymin, ymax):
        self.hist.GetXaxis().SetRangeUser(xmin, xmax)
        self.hist.GetYaxis().SetRangeUser(ymin, ymax)
        self.canvas.Update()
