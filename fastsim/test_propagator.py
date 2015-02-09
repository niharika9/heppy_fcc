import unittest
from geometry import Cylinder
from pfobjects import Particle
from propagator import straight_line 
from ROOT import TLorentzVector, TVector3

class TestPropagator(unittest.TestCase):
    def test_straightline(self):
        origin = TVector3(0,0,-1)
        particle = Particle( TLorentzVector(0.5, 0, 1, 2.), origin, 1)
        oecal = Cylinder('oecal', 1.8, 2.4)
        ohcal = Cylinder('ohcal', 2.9, 3.5)
        straight_line.propagate( particle, oecal )
        straight_line.propagate( particle, ohcal )
        self.assertEqual( len(particle.points), 3)


if __name__ == '__main__':
    unittest.main()
