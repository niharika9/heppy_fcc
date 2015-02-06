import unittest
from geometry import *

class TestCylinder(unittest.TestCase):
    def test_sub(self):
        cyl1 = Cylinder('cyl1', 1, 2)
        cyl2 = Cylinder('cyl2', 0.7, 1.5)
        subcyl = cyl1 - cyl2
        self.assertEqual(subcyl.name, 'cyl1-cyl2')
        self.assertEqual(subcyl.irad, 0.7)
        self.assertEqual(subcyl.orad, 1.)
        self.assertEqual(subcyl.iz, 1.5)
        self.assertEqual(subcyl.oz, 2.)
        # trying to subtract a cylinder with larger R
        self.assertRaises(ValueError, cyl1.__sub__, Cylinder('cyl3', 1.1, 2.))
        # trying to subtract a cylinder with larger z
        self.assertRaises(ValueError, cyl1.__sub__, Cylinder('cyl3', 0.9, 2.1))
        # trying to subtract a cylinder with non-zero inner dimensions
        self.assertRaises(ValueError, cyl1.__sub__, Cylinder('cyl3', 0.9, 2.1, 1., 1.))


class TestCMS(unittest.TestCase):
    def test_geom(self):
        cms = CMS()
        print cms.elements

if __name__ == '__main__':
    unittest.main()
