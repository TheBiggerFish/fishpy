import unittest

from fishpy.geometry import Circle, Point2D


class TestCircleProperties(unittest.TestCase):
    def setUp(self):
        self.circle = Circle(Point2D(0,0),4)

    def test_radius(self):
        self.circle.radius = 5
        self.assertEqual(self.circle.radius,5)
        try:
            self.circle.radius = -1
            self.assertNotEqual(self.circle.radius,-1)
        except ValueError:
            self.assertEqual(self.circle.radius,5)

    def test_diameter(self):
        self.assertEqual(self.circle.diameter,8)
        self.circle.radius = 5
        self.assertEqual(self.circle.diameter,10)
        self.circle.radius = 2.3
        self.assertEqual(self.circle.diameter,4.6)

    def test_circumference(self):
        self.assertAlmostEqual(self.circle.circumference,25.1327,4)
        self.circle.radius = 5
        self.assertAlmostEqual(self.circle.circumference,31.4159,4)
        self.circle.radius = 2.3
        self.assertAlmostEqual(self.circle.circumference,14.4513,4)

    def test_area(self):
        self.assertAlmostEqual(self.circle.area,50.2655,4)
        self.circle.radius = 5
        self.assertAlmostEqual(self.circle.area,78.5398,4)
        self.circle.radius = 2.3
        self.assertAlmostEqual(self.circle.area,16.6190,4)

class TestCircleDunderMethods(unittest.TestCase):
    def setUp(self):
        self.circle = Circle(Point2D(0,0),10)

    def test_contains(self):
        self.assertIn(Point2D(0,0),self.circle)
        self.assertIn(Point2D(-10,0),self.circle)
        self.assertIn(Point2D(7,7),self.circle)
        self.assertNotIn(Point2D(15,5),self.circle)
        self.assertNotIn(Point2D(9,9),self.circle)

    def test_repr(self):
        self.assertEqual(repr(self.circle),'Circle(Point2D(0,0),10)')

class TestCircleMethods(unittest.TestCase):
    def setUp(self):
        self.circle1 = Circle(Point2D(0,0),10)
        self.circle2 = Circle(Point2D(0,0),5)
        self.circle3 = Circle(Point2D(5,0),5)
        self.circle4 = Circle(Point2D(-15,0),5)
        self.circle5 = Circle(Point2D(20,0),5)

    def test_intersects(self):
        self.assertTrue(self.circle1.intersects(self.circle1))
        self.assertFalse(self.circle1.intersects(self.circle2))
        self.assertTrue(self.circle1.intersects(self.circle3))
        self.assertTrue(self.circle1.intersects(self.circle4))
        self.assertFalse(self.circle1.intersects(self.circle5))

    def test_intersecting_points(self):
        self.assertRaises(ValueError,Circle.intersecting_points,
                          self.circle1,self.circle1)
        self.assertIsNone(self.circle1.intersecting_points(self.circle2))
        self.assertTupleEqual(self.circle1.intersecting_points(self.circle3),
                              (Point2D(10,0),))
        self.assertTupleEqual(self.circle1.intersecting_points(self.circle4),
                              (Point2D(-10,0),))
        self.assertIsNone(self.circle1.intersecting_points(self.circle5))
        self.assertTupleEqual(self.circle2.intersecting_points(self.circle3),
                              (Point2D(2.5,-4.33012702),Point2D(2.5,4.33012702)))
