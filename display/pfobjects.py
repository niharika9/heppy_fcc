from ROOT import TPolyLine, TGraph, TArc
import numpy as np
import operator

class GTrajectory(object):
    def __init__(self, description):
        self.desc = description
        npoints = len(self.desc.points)
        self.graph_xy = TGraph(npoints)
        self.graph_yz = TGraph(npoints)
        self.graph_xz = TGraph(npoints)
        self.graphs = [self.graph_xy, self.graph_yz, self.graph_xz]
        def set_marker_style(graph):
            graph.SetMarkerStyle(8)
            graph.SetMarkerSize(0.5)
        set_marker_style(self.graph_xy)
        set_marker_style(self.graph_yz)
        set_marker_style(self.graph_xz)
        for i, point in enumerate(self.desc.points.values()):
            self.graph_xy.SetPoint( i, point.X(), point.Y() )
            self.graph_yz.SetPoint(i, point.Z(), point.Y() )
            self.graph_xz.SetPoint(i, point.Z(), point.X() )

    def set_color(self, color):
        for graph in self.graphs:
            graph.SetMarkerColor(color)
        
    def draw(self, projection, opt=''):
        if projection == 'xy':
            self.graph_xy.Draw(opt+"psame")
        elif projection == 'yz':
            self.graph_yz.Draw(opt+"psame")
        elif projection == 'xz':
            self.graph_xz.Draw(opt+"psame")            
        else:
            raise ValueError('implement drawing for projection ' + projection )

class GStraightTrajectory(GTrajectory):
    def __init__(self, description):
        super(GStraightTrajectory, self).__init__(description)

    def draw(self, projection):
        super(GStraightTrajectory, self).draw(projection, 'l')
   

class GHelixTrajectory(GTrajectory):
    
    def __init__(self, description):
        helix = description.helix
        self.helix_xy = TArc(helix.center_xy.X(),
                             helix.center_xy.Y(),
                             helix.rho, helix.phi_min, helix.phi_max)
        self.helix_xy.SetFillStyle(0)
        max_time = 2e-8
        npoints = 50
        self.graphline_yz = TGraph(npoints)
        self.graphline_xz = TGraph(npoints)
        for i, time in enumerate(np.linspace(0, max_time, npoints)):
            point = helix.point_at_time(time)
            self.graphline_yz.SetPoint(i, point.Z(), point.Y())
            self.graphline_xz.SetPoint(i, point.Z(), point.X())
        super(GHelixTrajectory, self).__init__(description)
        
    def draw(self, projection):
        if projection == 'xy':
            self.helix_xy.Draw("onlysame")
        elif projection == 'yz':
            self.graphline_yz.Draw("lsame")
        elif projection == 'xz':
            self.graphline_xz.Draw("lsame")
        else:
            raise ValueError('implement drawing for projection ' + projection )
        super(GHelixTrajectory, self).draw(projection)
        
        
if __name__ == '__main__':
    import math
    from heppy_fcc.fastsim.geometry import CMS
    from heppy_fcc.fastsim.vectors import Point
    from heppy_fcc.fastsim.propagator import StraightLinePropagator, HelixPropagator 
    from heppy_fcc.fastsim.toyevents import particles
    from heppy_fcc.display.core import Display
    from heppy_fcc.display.geometry import GDetector
    
    cms = CMS()
    gcms = GDetector(cms)

    display = Display()
    display.register(gcms, 0)
    # display.views['yz'].zoom(-1,1,-1,1)
    # display.views['xz'].zoom(-1,1,-1,1)

    colors = [1, 2, 3, 4, 8]
    
    slprop = StraightLinePropagator()
    helixprop = HelixPropagator()
    for i, ptc in enumerate( particles(5, 1, 0.3, math.pi/4., math.pi/4., 0.5, 1, Point(0,0,0))):
        # print ptc
        # ptc.p4.SetPhi(0.)
        is_neutral = abs(ptc.charge)<0.5
        prop = slprop
        TrajClass = GStraightTrajectory
        if not is_neutral:
            prop = helixprop
            TrajClass = GHelixTrajectory
        prop.propagate([ptc], cms.cylinders() )
        gtraj = TrajClass(ptc)
        gtraj.set_color( colors[i] )
        display.register(gtraj,1)
            

    display.draw()
