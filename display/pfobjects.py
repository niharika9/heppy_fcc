from ROOT import TPolyLine, TGraph, TArc, TEllipse
import numpy as np
import operator

class Blob(object):
    def __init__(self, cluster):
        radius = cluster.size
        # print radius
        color = 4
        max_energy = cluster.__class__.max_energy
        pos = cluster.position
        self.contour_xy = TEllipse(pos.X(), pos.Y(), radius)
        self.contour_yz = TEllipse(pos.Z(), pos.Y(), radius)   
        self.contour_xz = TEllipse(pos.Z(), pos.X(), radius)
        contours = [self.contour_xy, self.contour_yz, self.contour_xz]
        iradius = radius * cluster.energy / max_energy 
        self.inner_xy = TEllipse(pos.X(), pos.Y(), iradius)
        self.inner_yz = TEllipse(pos.Z(), pos.Y(), iradius)   
        self.inner_xz = TEllipse(pos.Z(), pos.X(), iradius)
        inners = [self.inner_xy, self.inner_yz, self.inner_xz]
        for contour in contours:
            contour.SetLineColor(color)
            contour.SetFillStyle(0)
        for inner in inners: 
            inner.SetFillColor(color)
            
    def draw(self, projection, opt=''):
        if projection == 'xy':
            self.contour_xy.Draw(opt+"psame")
            self.inner_xy.Draw(opt+"psame")
        elif projection == 'yz':
            self.contour_yz.Draw(opt+"psame")
            self.inner_yz.Draw(opt+"psame")
        elif projection == 'xz':
            self.contour_xz.Draw(opt+"psame")            
            self.inner_xz.Draw(opt+"psame")            
        else:
            raise ValueError('implement drawing for projection ' + projection )
        

class GTrajectory(object):
    def __init__(self, description):
        self.desc = description
        npoints = len(self.desc.points)
        self.graph_xy = TGraph(npoints)
        self.graph_yz = TGraph(npoints)
        self.graph_xz = TGraph(npoints)
        self.graphs = [self.graph_xy, self.graph_yz, self.graph_xz]
        def set_marker_style(graph):
            graph.SetMarkerStyle(4)
            graph.SetMarkerSize(0.5)
        set_marker_style(self.graph_xy)
        set_marker_style(self.graph_yz)
        set_marker_style(self.graph_xz)
        for i, point in enumerate(self.desc.points.values()):
            self.graph_xy.SetPoint( i, point.X(), point.Y() )
            self.graph_yz.SetPoint(i, point.Z(), point.Y() )
            self.graph_xz.SetPoint(i, point.Z(), point.X() )
        self.blobs = map(Blob, self.desc.clusters.values())            

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
        for blob in self.blobs: 
            blob.draw(projection, opt)
            
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
        #TODO this is patchy,need to access the last point, whatever its name
        max_time = description.helix.time_at_z(description.points.values()[-1].Z())
        npoints = 100
        
        self.graphline_xy = TGraph(npoints)
        self.graphline_yz = TGraph(npoints)
        self.graphline_xz = TGraph(npoints)
        for i, time in enumerate(np.linspace(0, max_time, npoints)):
            point = helix.point_at_time(time)
            self.graphline_xy.SetPoint(i, point.X(), point.Y())
            self.graphline_yz.SetPoint(i, point.Z(), point.Y())
            self.graphline_xz.SetPoint(i, point.Z(), point.X())
        super(GHelixTrajectory, self).__init__(description)
        
    def draw(self, projection):
        if projection == 'xy':
            # self.helix_xy.Draw("onlysame")
            self.graphline_xy.Draw("lsame")
        elif projection == 'yz':
            self.graphline_yz.Draw("lsame")
        elif projection == 'xz':
            self.graphline_xz.Draw("lsame")
        else:
            raise ValueError('implement drawing for projection ' + projection )
        super(GHelixTrajectory, self).draw(projection)
        

class GTrajectories(list):
    
    def __init__(self, particles):
        for ptc in particles:
            is_neutral = abs(ptc.charge)<0.5
            TrajClass = GStraightTrajectory if is_neutral else GHelixTrajectory
            gtraj = TrajClass(ptc)
            self.append(gtraj)
            # display.register(gtraj,1)

    def draw(self, projection):
        for traj in self:
            traj.draw(projection)
        
if __name__ == '__main__':
    import math
    from heppy_fcc.fastsim.geometry import CMS
    from heppy_fcc.fastsim.simulator import Simulator
    from heppy_fcc.fastsim.vectors import Point
    from heppy_fcc.fastsim.toyevents import particles
    from heppy_fcc.display.core import Display
    from heppy_fcc.display.geometry import GDetector
    
    cms = CMS()
    simulator = Simulator(cms)
    
    particles = list( particles(5, 1, 0.5, math.pi/5., 4*math.pi/5.,
                                10., 10., Point(0.5,0.5,0)) )
    simulator.simulate(particles)
    
    display = Display()
    gcms = GDetector(cms)
    display.register(gcms, 0)
    gtrajectories = GTrajectories(particles)
    display.register(gtrajectories,1)
    display.draw()
