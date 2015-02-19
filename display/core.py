from ROOT import TCanvas, TH1, TH2F
import operator
from heppy_fcc.fastsim.pfobjects import Cluster

class Display(object):
    
    def __init__(self, views=None):
        ViewPane.nviews = 0
        if not views:
            views = ['xy', 'yz', xz]
        self.views = dict()
        for view in views:
            self.views[view] = ViewPane("xy", "xy", 100, -5, 5, 100, -5, 5)

    def register(self, obj, layer, clearable=True):
        elems = [obj]
        if hasattr(obj, '__iter__'):
            elems = obj
        for elem in elems: 
            for view in self.views.values():
                view.register(elem, layer, clearable)

    def clear(self):
        for view in self.views.values():
            view.clear()
            
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
        self.locked = dict()
        self.__class__.nviews += 1 
        
    def register(self, obj, layer, clearable=True):
        self.registered[obj] = layer
        if not clearable:
            self.locked[obj] = layer
        #TODO might need to keep track of views in objects

    def clear(self):
        self.registered = dict(self.locked.items())
                
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
