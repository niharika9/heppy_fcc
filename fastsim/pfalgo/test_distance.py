import unittest
import itertools
from distance import Distance
from ROOT import TVector3

class Cluster(object):
    def __init__(self, typ, position, size=0.1):
        self.type = typ
        self.position = position
        self.size = size

class Track(object):
    def __init__(self, typ, ecal, hcal):
        self.type = typ
        self.points = dict(ecal=ecal, hcal=hcal)

ruler = Distance()

class TestDistance(unittest.TestCase):
    
    def test_typefan(self):
        c1 = Cluster('ecal', TVector3(1, 0, 0))
        c2 = Cluster('hcal', TVector3(1, 0, 0))
        tr = Track('track',
                   ecal=TVector3(1, 0, 0),
                   hcal=TVector3(1, 0, 0))
        elems = [c1, c2, tr]
        for ele in elems:
            link_type, link_ok, distance = ruler(ele, ele)
            # cannot link in same layer
            self.assertFalse(link_ok)
        for ele1, ele2 in itertools.combinations(elems, 2):
            link_type, link_ok, distance = ruler(ele1, ele2)
            self.assertTrue(link_ok)
        link_type, link_ok, distance = ruler(c2, c1)
        self.assertEqual(link_type, ('ecal','hcal'))
        
    def test_ecal_hcal(self):
        c1 = Cluster('ecal', TVector3(1, 0, 0), size=0.01)
        c2 = Cluster('hcal', TVector3(1, 0, 0), size=0.05)
        link_type, link_ok, distance = ruler(c1, c2)
        self.assertTrue(link_ok)
        self.assertEqual(distance, 0.)
        pos3 = TVector3(c1.position)
        pos3.RotateZ(0.059)
        c3 = Cluster('hcal', pos3, size=0.05)
        link_type, link_ok, distance = ruler(c1, c3)
        self.assertEqual(distance, 0.059)
        
        
        
        
if __name__ == '__main__':
    unittest.main()


    
