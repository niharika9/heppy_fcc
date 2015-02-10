import unittest
from geometry import SurfaceCylinder
from pfobjects import Particle
from propagator import straight_line
from vectors import LorentzVector, Point

class TestPropagator(unittest.TestCase):
    
    def test_straightline(self):
        origin = Point(0,0,0)
        cyl1 = SurfaceCylinder('cyl1', 1, 2)
        cyl2 = SurfaceCylinder('cyl2', 2, 1)

        particle = Particle( LorentzVector(1, 0, 1, 2.), origin, 1)
        straight_line.propagate_one( particle, cyl1 )
        straight_line.propagate_one( particle, cyl2 )
        self.assertEqual( len(particle.points), 3)
        # test extrapolation to barrel
        self.assertEqual( particle.points['cyl1'].Perp(), 1. )
        self.assertEqual( particle.points['cyl1'].Z(), 1. )
        # test extrapolation to endcap
        self.assertEqual( particle.points['cyl2'].Z(), 1. )
        
        # testing extrapolation to -z 
        particle = Particle( LorentzVector(1, 0, -1, 2.), origin, 1)
        # import pdb; pdb.set_trace()
        straight_line.propagate_one( particle, cyl1 )
        straight_line.propagate_one( particle, cyl2 )
        self.assertEqual( len(particle.points), 3)
        self.assertAlmostEqual( particle.points['cyl1'].Perp(), 1. )
        # test extrapolation to endcap
        self.assertAlmostEqual( particle.points['cyl1'].Z(), -1. )
        self.assertAlmostEqual( particle.points['cyl2'].Z(), -1. )

        # extrapolating from a vertex close to +endcap
        particle = Particle( LorentzVector(1, 0, 1, 2.),
                             Point(0,0,1.5), 1)
        straight_line.propagate_one( particle, cyl1 )
        self.assertAlmostEqual( particle.points['cyl1'].Perp(), 0.5 )
        
        # extrapolating from a vertex close to -endcap
        particle = Particle( LorentzVector(1, 0, -1, 2.),
                             Point(0,0,-1.5), 1)
        straight_line.propagate_one( particle, cyl1 )
        self.assertAlmostEqual( particle.points['cyl1'].Perp(), 0.5 )
        
        # extrapolating from a non-zero radius
        particle = Particle( LorentzVector(0, 0.5, 1, 2.),
                             Point(0,0.5,0), 1)
        straight_line.propagate_one( particle, cyl1 )
        self.assertAlmostEqual( particle.points['cyl1'].Perp(), 1. )
        self.assertAlmostEqual( particle.points['cyl1'].Z(), 1. )
        
 
if __name__ == '__main__':
    unittest.main()
