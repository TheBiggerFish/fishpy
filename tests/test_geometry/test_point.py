import unittest

from fishpy.geometry import Point


class TestPointStaticMethods(unittest.TestCase):
    def test_origin(self):
        self.assertEqual(Point.origin(1),Point(0))
        self.assertEqual(Point.origin(2),Point(0,0))
        self.assertEqual(Point.origin(3),Point(0,0,0))
        self.assertEqual(Point.origin(4),Point(0,0,0,0))
        self.assertEqual(Point.origin(5),Point(0,0,0,0,0))

        self.assertNotEqual(Point.origin(5),Point(0,0,0,0,1))
        self.assertNotEqual(Point.origin(5),Point(0,0,0,0,0,1))

class TestPointDunderMethods(unittest.TestCase):
    def setUp(self):
        self.p1 = Point(1,1)
        self.p2 = Point(1,-5)
        self.p3 = Point(0,2)
        self.p4 = Point(-3,5)

    def test_eq(self):
        self.assertFalse(self.p1==self.p2)
        self.assertTrue(self.p1==Point(1,1))
        self.assertTrue(self.p2==Point(1,-5))
        self.assertTrue(self.p3==Point(0,2))
        self.assertTrue(self.p4==Point(-3,5))

    def test_add(self):
        self.assertEqual(self.p1+self.p1,Point(2,2))
        self.assertEqual(self.p2+self.p3,Point(1,-3))
        self.assertEqual(self.p2+self.p4,Point(-2,0))
        self.assertEqual(self.p1+self.p3,Point(1,3))

    def test_sub(self):
        self.assertEqual(self.p1-self.p1,Point(0,0))
        self.assertEqual(self.p3-self.p2,Point(-1,7))
        self.assertEqual(self.p4-self.p2,Point(-4,10))
        self.assertEqual(self.p1-self.p3,Point(1,-1))

    def test_neg(self):
        self.assertEqual(-self.p1,Point(-1,-1))
        self.assertEqual(-self.p2,Point(-1,5))
        self.assertEqual(-self.p3,Point(0,-2))
        self.assertEqual(-self.p4,Point(3,-5))

    def test_lt(self):
        self.assertTrue(Point(0,0) < self.p1)
        self.assertTrue(Point(-3,0) < self.p3)
        self.assertFalse(Point(0,1) < self.p3)
        self.assertFalse(Point(-3,5) < self.p4)

    def test_le(self):
        self.assertTrue(Point(1,0) <= self.p1)
        self.assertTrue(Point(-3,5) <= self.p4)
        self.assertTrue(Point(0,1) <= self.p3)
        self.assertFalse(Point(6,6) <= self.p4)

    def test_str(self):
        self.assertEqual(str(self.p1),'(1, 1)')
        self.assertEqual(str(self.p2),'(1, -5)')
        self.assertEqual(str(self.p3),'(0, 2)')
        self.assertEqual(str(self.p4),'(-3, 5)')

    def test_repr(self):
        self.assertEqual(repr(self.p1),'Point(1, 1)')
        self.assertEqual(repr(self.p2),'Point(1, -5)')
        self.assertEqual(repr(self.p3),'Point(0, 2)')
        self.assertEqual(repr(self.p4),'Point(-3, 5)')

    def test_mul(self):
        self.assertEqual(self.p1*3,Point(3,3))
        self.assertEqual(self.p2*-1,Point(-1,5))
        self.assertEqual(self.p3*2,Point(0,4))
        self.assertEqual(self.p4*0.5,Point(-1.5,2.5))

    def test_true_div(self):
        self.assertEqual(self.p1/2,Point(0.5,0.5))
        self.assertEqual(self.p2/1,Point(1,-5))
        self.assertEqual(self.p3/4,Point(0,0.5))
        self.assertEqual(self.p4/-1,Point(3,-5))
        self.assertRaises(ZeroDivisionError,Point.__truediv__,self.p1,0)

    def test_floor_div(self):
        pass

    def test_mod(self):
        pass

    def test_abs(self):
        pass

    def test_iter(self):
        pass

    def test_gt(self):
        pass

    def test_ge(self):
        pass

    def test_ne(self):
        pass

class TestPointMethods(unittest.TestCase):
    def setUp(self):
        self.p1 = Point(1,1)
        self.p2 = Point(1,-5)
        self.p3 = Point(0,2)
        self.p4 = Point(-3,5)

    def test_copy(self):
        self.p2 = self.p1.copy()
        self.assertEqual(self.p2,self.p1)
        self.p2.x = 0
        self.assertNotEqual(self.p2,self.p1)

    def test_manhattan_distance(self):
        self.assertEqual(self.p1.manhattan_distance(self.p2),6)
        self.assertEqual(self.p2.manhattan_distance(self.p3),8)
        self.assertEqual(self.p3.manhattan_distance(self.p4),6)
        self.assertEqual(self.p4.manhattan_distance(self.p1),8)

    def test_euclidean_distance(self):
        self.assertEqual(self.p1.euclidean_distance(self.p2),6)
        self.assertEqual(self.p2.euclidean_distance(self.p3),50**0.5)
        self.assertEqual(self.p3.euclidean_distance(self.p4),18**0.5)
        self.assertEqual(self.p4.euclidean_distance(self.p1),32**0.5)

    def test_midpoint(self):
        self.assertEqual(self.p1.midpoint(self.p2),Point(1,-2))
        self.assertEqual(self.p2.midpoint(self.p3),Point(0.5,-1.5))
        self.assertEqual(self.p3.midpoint(self.p4),Point(-1.5,3.5))
        self.assertEqual(self.p4.midpoint(self.p1),Point(-1,3))

    def test_bounded_filter(self):
        pass

    def test_in_bounds(self):
        self.assertTrue(self.p1.in_bounds(lower_bound=Point(0,0),upper_bound=Point(5,5)))
        self.assertTrue(self.p2.in_bounds(lower_bound=Point(-1,-5),upper_bound=Point(10,10)))
        self.assertFalse(self.p3.in_bounds(lower_bound=Point(-10,-10),upper_bound=Point(0,0)))
        self.assertFalse(self.p4.in_bounds(lower_bound=Point(-5,-10),upper_bound=self.p4))

    def test_as_tuple(self):
        self.assertSequenceEqual(self.p1.as_tuple(),(1,1))
        self.assertSequenceEqual(self.p2.as_tuple(),(1,-5))
        self.assertSequenceEqual(self.p3.as_tuple(),(0,2))
        self.assertSequenceEqual(self.p4.as_tuple(),(-3,5))

    def test_random(self):
        self.assertTrue(Point.random(lower_bound=self.p1,
                                     upper_bound=Point(5,5)
                                    ).in_bounds(self.p1,Point(5,5)))


if __name__ == '__main__':
    unittest.main()
