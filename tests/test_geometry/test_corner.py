import unittest

from fishpy.geometry import Corner, Point2D


class TestCornerMethods(unittest.TestCase):
    def setUp(self):
        p1 = Point2D(0,0)
        p2 = Point2D(1,1)
        p3 = Point2D(1,0)
        p4 = Point2D(0,1)
        p5 = Point2D(-1,1)
        p6 = Point2D(1,-1)
        p7 = Point2D(-1,-1)
        p8 = Point2D(-1,0)
        p9 = Point2D(0,-1)

        self.corner1 = Corner(p1,p2,p3)
        self.corner2 = Corner(p1,p3,p4)
        self.corner3 = Corner(p1,p3,p9)
        self.corner4 = Corner(p7,p2,p6)
        self.corner5 = Corner(p5,p8,p3)
        self.corner6 = Corner(p1,p8,p3)

    def test_get_angle(self):
        self.assertAlmostEqual(self.corner1.get_angle(),45)
        self.assertAlmostEqual(self.corner2.get_angle(),90)
        self.assertAlmostEqual(self.corner3.get_angle(),90)
        self.assertAlmostEqual(self.corner4.get_angle(),45)
        self.assertAlmostEqual(self.corner5.get_angle(),63.43495)
        self.assertAlmostEqual(self.corner6.get_angle(),180)
