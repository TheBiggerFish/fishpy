import unittest

from fishpy.geometry import LatticePoint


class TestLatticePointProperties(unittest.TestCase):
    def setUp(self):
        self.p1 = LatticePoint(2, 4)

    def test_x(self):
        self.assertEqual(self.p1.x, 2)
        self.p1.x = 1
        self.assertEqual(self.p1.x, 1)
        try:
            self.p1.x = 0.5
            self.assertNotEqual(self.p1.x, 0.5)
        except TypeError:
            self.assertEqual(self.p1.x, 1)

    def test_y(self):
        self.assertEqual(self.p1.y, 4)
        self.p1.y = 2
        self.assertEqual(self.p1.y, 2)
        try:
            self.p1.y = 0.5
            self.assertNotEqual(self.p1.y, 0.5)
        except TypeError:
            self.assertEqual(self.p1.y, 2)


class TestLatticePointStaticMethods(unittest.TestCase):
    def setUp(self):
        self.p1 = LatticePoint(1, 1)

    def test_random(self):
        self.assertTrue(LatticePoint.random(lower_bound=self.p1,
                                            upper_bound=LatticePoint(5, 5)
                                            ).in_bounds(self.p1, LatticePoint(6, 6)))


class TestLatticePointDunderMethods(unittest.TestCase):
    def setUp(self):
        self.p1 = LatticePoint(1, 1)
        self.p2 = LatticePoint(1, -5)
        self.p3 = LatticePoint(0, 2)
        self.p4 = LatticePoint(-3, 5)

    def test_init(self):
        self.assertRaises(TypeError, LatticePoint, 5, 2.5)
        self.assertRaises(TypeError, LatticePoint, 0, 0.001)

    def test_add(self):
        self.assertEqual(self.p1+self.p1, LatticePoint(2, 2))
        self.assertEqual(self.p2+self.p3, LatticePoint(1, -3))
        self.assertEqual(self.p2+self.p4, LatticePoint(-2, 0))
        self.assertEqual(self.p1+self.p3, LatticePoint(1, 3))

    def test_sub(self):
        self.assertEqual(self.p1-self.p1, LatticePoint(0, 0))
        self.assertEqual(self.p3-self.p2, LatticePoint(-1, 7))
        self.assertEqual(self.p4-self.p2, LatticePoint(-4, 10))
        self.assertEqual(self.p1-self.p3, LatticePoint(1, -1))

    def test_neg(self):
        self.assertEqual(-self.p1, LatticePoint(-1, -1))
        self.assertEqual(-self.p2, LatticePoint(-1, 5))
        self.assertEqual(-self.p3, LatticePoint(0, -2))
        self.assertEqual(-self.p4, LatticePoint(3, -5))

    def test_mul(self):
        self.assertEqual(self.p1*3, LatticePoint(3, 3))
        self.assertEqual(self.p2*-1, LatticePoint(-1, 5))
        self.assertEqual(self.p3*2, LatticePoint(0, 4))
        self.assertRaises(TypeError, LatticePoint.__mul__, self.p4, 0.5)

    def test_truediv(self):
        self.assertEqual(self.p3/2, LatticePoint(0, 1))
        self.assertEqual(LatticePoint(10, 10)//2, LatticePoint(5, 5))
        self.assertRaises(ValueError, LatticePoint.__truediv__, self.p1, 2)
        self.assertRaises(ValueError, LatticePoint.__truediv__, self.p4, 5)

    def test_floordiv(self):
        self.assertEqual(self.p1//4, LatticePoint(0, 0))
        self.assertEqual(self.p2//1, LatticePoint(1, -5))
        self.assertEqual(self.p3//2, LatticePoint(0, 1))
        self.assertEqual(self.p4//-1, LatticePoint(3, -5))

    def test_abs(self):
        self.assertEqual(abs(-self.p1), LatticePoint(1, 1))
        self.assertEqual(abs(self.p2), LatticePoint(1, 5))
        self.assertEqual(abs(-self.p3), LatticePoint(0, 2))
        self.assertEqual(abs(self.p4), LatticePoint(3, 5))

    def test_repr(self):
        self.assertEqual(repr(self.p1), 'LatticePoint(1, 1)')
        self.assertEqual(repr(self.p2), 'LatticePoint(1, -5)')
        self.assertEqual(repr(self.p3), 'LatticePoint(0, 2)')
        self.assertEqual(repr(self.p4), 'LatticePoint(-3, 5)')


class TestLatticePointMethods(unittest.TestCase):
    def setUp(self):
        self.p1 = LatticePoint(1, 1)
        self.p2 = LatticePoint(1, -5)
        self.p3 = LatticePoint(0, 2)
        self.p4 = LatticePoint(-3, 5)

    def test_get_adjacent_points(self):
        self.assertSetEqual(set(self.p1.get_adjacent_points(diagonals=False)),
                            {LatticePoint(0, 1), LatticePoint(1, 0), LatticePoint(2, 1),
                            LatticePoint(1, 2)})
        self.assertSetEqual(set(self.p3.get_adjacent_points(diagonals=True)),
                            {LatticePoint(-1, 1), LatticePoint(0, 1), LatticePoint(1, 1),
                            LatticePoint(-1, 2), LatticePoint(1,
                                                              2), LatticePoint(-1, 3),
                            LatticePoint(0, 3), LatticePoint(1, 3)})
        self.assertSetEqual(set(self.p4.get_adjacent_points(diagonals=True,
                                                            lower_bound=LatticePoint(-3, 5))),
                            {LatticePoint(-2, 5), LatticePoint(-3, 6), LatticePoint(-2, 6)})
        self.assertSetEqual(set(self.p2.get_adjacent_points(diagonals=True,
                                                            lower_bound=LatticePoint(
                                                                0, -6),
                                                            upper_bound=LatticePoint(1, -5))),
                            {LatticePoint(0, -6)})

    def test_lattice_midpoint(self):
        self.assertEqual(self.p1.lattice_midpoint(
            self.p2), LatticePoint(1, -2))
        self.assertEqual(self.p2.lattice_midpoint(
            self.p3), LatticePoint(0, -2))
        self.assertEqual(self.p3.lattice_midpoint(
            self.p4), LatticePoint(-2, 3))
        self.assertEqual(self.p4.lattice_midpoint(
            self.p1), LatticePoint(-1, 3))

    def test_copy(self):
        test_point = self.p1.copy()
        self.assertEqual(test_point, self.p1)
        test_point += LatticePoint(1, 1)
        self.assertNotEqual(test_point, self.p1)

    def test_up(self):
        self.assertEqual(self.p1.up(), LatticePoint(1, 2))
        self.assertEqual(self.p2.up(), LatticePoint(1, -4))
        self.assertEqual(self.p3.up(), LatticePoint(0, 3))
        self.assertEqual(self.p4.up(), LatticePoint(-3, 6))

    def test_down(self):
        self.assertEqual(self.p1.down(), LatticePoint(1, 0))
        self.assertEqual(self.p2.down(), LatticePoint(1, -6))
        self.assertEqual(self.p3.down(), LatticePoint(0, 1))
        self.assertEqual(self.p4.down(), LatticePoint(-3, 4))

    def test_left(self):
        self.assertEqual(self.p1.left(), LatticePoint(0, 1))
        self.assertEqual(self.p2.left(), LatticePoint(0, -5))
        self.assertEqual(self.p3.left(), LatticePoint(-1, 2))
        self.assertEqual(self.p4.left(), LatticePoint(-4, 5))

    def test_right(self):
        self.assertEqual(self.p1.right(), LatticePoint(2, 1))
        self.assertEqual(self.p2.right(), LatticePoint(2, -5))
        self.assertEqual(self.p3.right(), LatticePoint(1, 2))
        self.assertEqual(self.p4.right(), LatticePoint(-2, 5))
