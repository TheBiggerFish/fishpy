import unittest

from fishpy.geometry import Ellipse, Point2D


class TestEllipseProperties(unittest.TestCase):
    def setUp(self):
        p1 = Point2D(-10,0)
        p2 = Point2D(10,0)
        p3 = Point2D(0,0)
        p4 = Point2D(0,10)

        self.ellipse1 = Ellipse(p1,p2,Point2D(15,0))
        self.ellipse2 = Ellipse(p1,p3,p2)
        self.ellipse3 = Ellipse(p3,p4,Point2D(0,-5))
        self.ellipse4 = Ellipse(p2,p4,Point2D(0,11))

    def test_major_axis(self):
        self.assertEqual(self.ellipse1.major_axis,30)
        self.assertEqual(self.ellipse2.major_axis,30)
        self.assertEqual(self.ellipse3.major_axis,20)
        self.assertEqual(self.ellipse4.major_axis,221**0.5+1)

    def test_minor_axis(self):
        self.assertAlmostEqual(self.ellipse1.minor_axis,500**0.5)
        self.assertAlmostEqual(self.ellipse2.minor_axis,800**0.5)
        self.assertAlmostEqual(self.ellipse3.minor_axis,300**0.5)
        self.assertAlmostEqual(self.ellipse4.minor_axis,
                               ((self.ellipse4.major_axis)**2-200)**0.5)

    def test_angle(self):
        self.assertEqual(self.ellipse1.angle,0)
        self.assertEqual(self.ellipse2.angle,0)
        self.assertEqual(self.ellipse3.angle,90)
        self.assertEqual(self.ellipse4.angle,45)

    def test_center(self):
        self.assertEqual(self.ellipse1.center,Point2D(0,0))
        self.assertEqual(self.ellipse2.center,Point2D(-5,0))
        self.assertEqual(self.ellipse3.center,Point2D(0,5))
        self.assertEqual(self.ellipse4.center,Point2D(5,5))

class TestEllipseDunderMethods(unittest.TestCase):
    def setUp(self):
        p1 = Point2D(-10,0)
        p2 = Point2D(10,0)
        p3 = Point2D(0,0)
        p4 = Point2D(0,10)

        self.ellipse1 = Ellipse(p1,p2,Point2D(15,0))
        self.ellipse2 = Ellipse(p1,p3,p2)
        self.ellipse3 = Ellipse(p3,p4,Point2D(0,-5))
        self.ellipse4 = Ellipse(p2,p4,Point2D(0,11))

    def test_contains(self):
        pass

class TestEllipseMethods(unittest.TestCase):
    pass
