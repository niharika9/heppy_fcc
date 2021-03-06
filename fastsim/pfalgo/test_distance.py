import unittest
import itertools
from distance import Distance
from links import Element
from heppy_fcc.fastsim.pfobjects import Cluster, Track
from heppy_fcc.fastsim.path import StraightLine

from ROOT import TVector3, TLorentzVector
 
ruler = Distance()

class TestDistance(unittest.TestCase):
    
    def test_layerfan(self):
        c1 = Cluster(10, TVector3(1, 0, 0), 1., 'ecal_in')
        c2 = Cluster(20, TVector3(1, 0, 0), 1., 'hcal_in')
        p3 = c1.position.Unit()*100.
        p4 = TLorentzVector()
        p4.SetVectM(p3, 1.)
        path = StraightLine(p4, TVector3(0,0,0))
        charge = 1.
        tr = Track(p3, charge, path)
        tr.path.points['ecal_in'] = c1.position
        tr.path.points['hcal_in'] = c2.position
        elems = [c1, c2, tr]
        for ele in elems:
            link_type, link_ok, distance = ruler(ele, ele)
            if ele!=tr:
                self.assertTrue(link_ok)
            elif ele==tr:
                self.assertFalse(link_ok)
        for ele1, ele2 in itertools.combinations(elems, 2):
            link_type, link_ok, distance = ruler(ele1, ele2)
            self.assertTrue(link_ok)
        link_type, link_ok, distance = ruler(c2, c1)
        self.assertEqual(link_type, ('ecal_in','hcal_in'))
        
    def test_ecal_hcal(self):
        c1 = Cluster(10, TVector3(1, 0, 0), 4., 'ecal_in')
        c2 = Cluster(20, TVector3(1, 0, 0), 4., 'hcal_in')
        link_type, link_ok, distance = ruler(c1, c2)
        self.assertTrue(link_ok)
        self.assertEqual(distance, 0.)
        pos3 = TVector3(c1.position)
        pos3.RotateZ(0.059)
        c3 = Cluster(30, pos3, 5, 'hcal_in')
        link_type, link_ok, distance = ruler(c1, c3)
        self.assertEqual(distance, 0.059)
        
        
        
        
if __name__ == '__main__':
    unittest.main()


    
