import unittest
import math

from fishpy.geometry import Point2D


class TestPoint2dDunderMethods(unittest.TestCase):
    def setUp(self):
        self.p1 = Point2D(1,1)
        self.p2 = Point2D(1,-5)
        self.p3 = Point2D(0,2)
        self.p4 = Point2D(-3,5)

    def test_add(self):
        self.assertEqual(self.p1+self.p1,Point2D(2,2))
        self.assertEqual(self.p2+self.p3,Point2D(1,-3))
        self.assertEqual(self.p2+self.p4,Point2D(-2,0))
        self.assertEqual(self.p1+self.p3,Point2D(1,3))

    def test_sub(self):
        self.assertEqual(self.p1-self.p1,Point2D(0,0))
        self.assertEqual(self.p3-self.p2,Point2D(-1,7))
        self.assertEqual(self.p4-self.p2,Point2D(-4,10))
        self.assertEqual(self.p1-self.p3,Point2D(1,-1))

    def test_neg(self):
        self.assertEqual(-self.p1,Point2D(-1,-1))
        self.assertEqual(-self.p2,Point2D(-1,5))
        self.assertEqual(-self.p3,Point2D(0,-2))
        self.assertEqual(-self.p4,Point2D(3,-5))

    def test_eq(self):
        self.assertFalse(self.p1==self.p2)
        self.assertTrue(self.p1==Point2D(1,1))
        self.assertTrue(self.p2==Point2D(1,-5))
        self.assertTrue(self.p3==Point2D(0,2))
        self.assertTrue(self.p4==Point2D(-3,5))

    def test_ne(self):
        self.assertTrue(self.p1!=self.p2)
        self.assertFalse(self.p1!=Point2D(1,1))
        self.assertFalse(self.p2!=Point2D(1,-5))
        self.assertTrue(self.p3!=Point2D(1,3))
        self.assertTrue(self.p4!=Point2D(-2,6))

    def test_lt(self):
        self.assertTrue(Point2D(0,0) < self.p1)
        self.assertTrue(Point2D(-3,0) < self.p3)
        self.assertFalse(Point2D(0,1) < self.p3)
        self.assertFalse(Point2D(-3,5) < self.p4)

    def test_gt(self):
        self.assertFalse(Point2D(0,0) > self.p1)
        self.assertFalse(Point2D(-3,0) > self.p3)
        self.assertTrue(Point2D(0,1) > self.p3)
        self.assertTrue(Point2D(-3,6) > self.p4)
        self.assertFalse(self.p1 > self.p1)

    def test_le(self):
        self.assertTrue(Point2D(1,0) <= self.p1)
        self.assertTrue(Point2D(-3,5) <= self.p4)
        self.assertTrue(Point2D(0,1) <= self.p3)
        self.assertFalse(Point2D(6,6) <= self.p4)

    def test_ge(self):
        self.assertFalse(Point2D(0,0) >= self.p1)
        self.assertTrue(Point2D(8,1) >= self.p3)
        self.assertTrue(Point2D(-1,2) >= self.p3)
        self.assertTrue(Point2D(-3,5) >= self.p4)
        self.assertFalse(self.p1 > self.p1)

    def test_hash(self):
        test_dict = {self.p1:1,self.p2:2,self.p3:3,self.p4:4}
        self.assertEqual(test_dict[self.p1],1)
        self.assertEqual(test_dict[self.p2],2)
        self.assertEqual(test_dict[self.p3],3)
        self.assertEqual(test_dict[self.p4],4)

    def test_str(self):
        self.assertEqual(str(self.p1),'(1,1)')
        self.assertEqual(str(self.p2),'(1,-5)')
        self.assertEqual(str(self.p3),'(0,2)')
        self.assertEqual(str(self.p4),'(-3,5)')

    def test_repr(self):
        self.assertEqual(repr(self.p1),'Point2D(1,1)')
        self.assertEqual(repr(self.p2),'Point2D(1,-5)')
        self.assertEqual(repr(self.p3),'Point2D(0,2)')
        self.assertEqual(repr(self.p4),'Point2D(-3,5)')

    def test_mul(self):
        self.assertEqual(self.p1*3,Point2D(3,3))
        self.assertEqual(self.p2*-1,Point2D(-1,5))
        self.assertEqual(self.p3*2,Point2D(0,4))
        self.assertEqual(self.p4*0.5,Point2D(-1.5,2.5))

    def test_true_div(self):
        self.assertEqual(self.p1/2,Point2D(0.5,0.5))
        self.assertEqual(self.p2/1,Point2D(1,-5))
        self.assertEqual(self.p3/4,Point2D(0,0.5))
        self.assertEqual(self.p4/-1,Point2D(3,-5))
        self.assertRaises(ZeroDivisionError,Point2D.__truediv__,self.p1,0)

    def test_floor_div(self):
        self.assertEqual(self.p1//2,Point2D(0,0))
        self.assertEqual(self.p2//1,Point2D(1,-5))
        self.assertEqual(self.p3//4,Point2D(0,0))
        self.assertEqual(self.p4//-1,Point2D(3,-5))
        self.assertRaises(ZeroDivisionError,Point2D.__truediv__,self.p1,0)

    def test_mod(self):
        self.assertEqual(self.p1 % Point2D(5,5),self.p1)
        self.assertEqual(self.p2 % Point2D(2,2),Point2D(1,1))
        self.assertEqual(self.p3 % Point2D(1,1),Point2D(0,0))
        self.assertEqual(self.p4 % Point2D(4,3),Point2D(1,2))

    def test_abs(self):
        self.assertEqual(abs(-self.p1),Point2D(1,1))
        self.assertEqual(abs(self.p2),Point2D(1,5))
        self.assertEqual(abs(-self.p3),Point2D(0,2))
        self.assertEqual(abs(self.p4),Point2D(3,5))

    def test_floor(self):
        self.assertEqual(math.floor(Point2D(0.57,7.13)),Point2D(0,7))
        self.assertEqual(math.floor(Point2D(3.14,2.81)),Point2D(3,2))
        self.assertEqual(math.floor(Point2D(0.01,0.99)),Point2D(0,0))
        self.assertEqual(math.floor(Point2D(9.12,-1.1)),Point2D(9,-2))

    def test_ceil(self):
        self.assertEqual(math.ceil(Point2D(0.57,7.13)),Point2D(1,8))
        self.assertEqual(math.ceil(Point2D(3.14,2.81)),Point2D(4,3))
        self.assertEqual(math.ceil(Point2D(0.01,0.99)),Point2D(1,1))
        self.assertEqual(math.ceil(Point2D(9.12,-1.1)),Point2D(10,-1))

class TestPoint2dMethods(unittest.TestCase):
    def setUp(self):
        self.p1 = Point2D(1,1)
        self.p2 = Point2D(1,-5)
        self.p3 = Point2D(0,2)
        self.p4 = Point2D(-3,5)

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
        self.assertEqual(self.p1.midpoint(self.p2),Point2D(1,-2))
        self.assertEqual(self.p2.midpoint(self.p3),Point2D(0.5,-1.5))
        self.assertEqual(self.p3.midpoint(self.p4),Point2D(-1.5,3.5))
        self.assertEqual(self.p4.midpoint(self.p1),Point2D(-1,3))

    def test_in_bounds(self):
        self.assertTrue(self.p1.in_bounds(lower_bound=Point2D(0,0),upper_bound=Point2D(5,5)))
        self.assertTrue(self.p2.in_bounds(lower_bound=Point2D(-1,-5),upper_bound=Point2D(10,10)))
        self.assertFalse(self.p3.in_bounds(lower_bound=Point2D(-10,-10),upper_bound=Point2D(0,0)))
        self.assertFalse(self.p4.in_bounds(lower_bound=Point2D(-5,-10),upper_bound=self.p4))

    def test_copy(self):
        test_point = self.p1.copy()
        self.assertEqual(test_point,self.p1)
        test_point.x = 0
        self.assertNotEqual(test_point,self.p1)

    def test_as_tuple(self):
        self.assertSequenceEqual(self.p1.as_tuple(),(1,1))
        self.assertSequenceEqual(self.p2.as_tuple(),(1,-5))
        self.assertSequenceEqual(self.p3.as_tuple(),(0,2))
        self.assertSequenceEqual(self.p4.as_tuple(),(-3,5))

    def test_is_above(self):
        self.assertFalse(self.p1.is_above(self.p1))
        self.assertFalse(self.p2.is_above(self.p3))
        self.assertTrue(self.p3.is_above(self.p1))
        self.assertTrue(self.p4.is_above(self.p2))

    def test_is_below(self):
        self.assertFalse(self.p1.is_below(self.p1))
        self.assertTrue(self.p2.is_below(self.p3))
        self.assertFalse(self.p3.is_below(self.p1))
        self.assertFalse(self.p4.is_below(self.p2))

    def test_is_left(self):
        self.assertFalse(self.p1.is_left_of(self.p1))
        self.assertFalse(self.p2.is_left_of(self.p4))
        self.assertTrue(self.p3.is_left_of(self.p1))
        self.assertTrue(self.p4.is_left_of(self.p3))

    def test_is_right(self):
        self.assertFalse(self.p1.is_right_of(self.p1))
        self.assertFalse(self.p2.is_right_of(self.p1))
        self.assertTrue(self.p3.is_right_of(self.p4))
        self.assertTrue(self.p4.is_right_of(Point2D(-10,0)))

    def test_random(self):
        random_point = Point2D.random(lower_bound=self.p1,upper_bound=Point2D(5,5))
        self.assertTrue(random_point.in_bounds(self.p1,Point2D(6,6)))


if __name__ == '__main__':
    unittest.main()
