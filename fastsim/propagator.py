from vectors import Point

class StraightLinePropagator(object):        
    
    def propagate(self, particle, cylinder):
        point = Point(1,1,1)
        udir = particle.p4.Vect().Unit()
        origin = particle.vertex
        if udir.Z():
            length = (cylinder.oz - origin.Z())/udir.Z()
            destination = origin + udir * length
            print length
            print destination.X(), destination.Y(), destination.Z()
        particle.points[cylinder.name] = point

straight_line = StraightLinePropagator()

