import unittest
from geometry import *

class TestCylinder(unittest.TestCase):
    def test_sub(self):
        cyl1 = SurfaceCylinder('cyl1', 1, 2)
        cyl2 = SurfaceCylinder('cyl2', 0.7, 1.5)
        subcyl = VolumeCylinder( 'subcyl', cyl1, cyl2 ) 
        self.assertEqual(subcyl.inner.rad, 0.7)
        self.assertEqual(subcyl.outer.rad, 1.)
        self.assertEqual(subcyl.inner.z, 1.5)
        self.assertEqual(subcyl.outer.z, 2.)
        # inner cylinder larger than the outer one 
        self.assertRaises(ValueError,
                          VolumeCylinder, 'test', cyl2, cyl1 )
        # forgot name 
        self.assertRaises(ValueError,
                          VolumeCylinder, cyl2, cyl1 )


class TestCMS(unittest.TestCase):
    def test_geom(self):
        cms = CMS()
        print cms.elements

if __name__ == '__main__':
    unittest.main()
