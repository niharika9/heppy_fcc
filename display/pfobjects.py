from ROOT import TPolyLine, TGraph
import numpy as np
import operator

class GTrajectory(object):
    def __init__(self, description):
        self.desc = description
        npoints = len(self.desc.points)
        self.line_rhophi = TGraph(npoints)
        self.line_rhoz = TGraph(npoints)
        def set_line_style(line):
            line.SetMarkerStyle(8)
            line.SetMarkerSize(0.6)
        set_line_style(self.line_rhophi)
        set_line_style(self.line_rhoz)
        for i, point in enumerate(self.desc.points.values()):
            self.line_rhophi.SetPoint( i, point.X(), point.Y() )
            self.line_rhoz.SetPoint(i, point.Z(), point.Perp() )

    def draw(self, projection):
        if projection == 'rhophi':
            self.line_rhophi.Draw("lpsame")
        elif projection == 'rhoz':
            self.line_rhoz.Draw("lpsame")
        else:
            raise ValueError('implement drawing for projection ' + projection )

if __name__ == '__main__':
    import math
    from heppy_fcc.fastsim.geometry import CMS
    from heppy_fcc.fastsim.vectors import Point
    from heppy_fcc.fastsim.propagator import StraightLinePropagator 
    from heppy_fcc.fastsim.toyevents import particles
    from heppy_fcc.display.core import Display
    from heppy_fcc.display.geometry import GDetector
    
    cms = CMS()
    gcms = GDetector(cms)

    display = Display()
    display.register(gcms, 0)

    slprop = StraightLinePropagator()
    
    for ptc in particles(1, 0., 0., 0., math.pi, 10, 50):
        print ptc
        slprop.propagate([ptc], cms.cylinders() )
        gtraj = GTrajectory(ptc)
        display.register(gtraj,1)

    display.draw()
