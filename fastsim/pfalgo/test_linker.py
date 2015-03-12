import unittest
from linker import Linker

def distance(ele1, ele2):
    dist = abs(ele1-ele2)
    return dist<3., dist

class Element(int):
    def __init__(self, val):
        self.linked = []
        super(Element, self).__init__(val)

class TestLinker(unittest.TestCase):

    def test_link_1(self):
        elements = map(Element, range(10))
        linker = Linker(elements, distance)
        distances = linker.links.values()
        self.assertTrue( max(distances)==2 )
        self.assertEqual( elements[0].linked, [elements[1], elements[2]])
        self.assertEqual( linker.links[2,4], 2)
        self.assertIsNone( linker.links.get((2,5), None))
        
if __name__ == '__main__':
    unittest.main()



