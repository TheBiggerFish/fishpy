
import unittest

from fishpy.pathfinding.grid import Cell

class TestCell(unittest.TestCase):
    def setUp(self):
        self.cell = Cell(2, 3, 'A')

    def test_initialization(self):
        self.assertEqual(self.cell.x, 2)
        self.assertEqual(self.cell.y, 3)
        self.assertEqual(self.cell.value, 'A')

    def test_repr(self):
        expected_repr = "Cell(x=2, y=3, value='A')"
        self.assertEqual(repr(self.cell), expected_repr)

    def test_copy(self):
        cell_copy = self.cell.copy()
        self.assertEqual(cell_copy.x, self.cell.x)
        self.assertEqual(cell_copy.y, self.cell.y)
        self.assertEqual(cell_copy.value, self.cell.value)
        self.assertIsNot(cell_copy, self.cell)  # Ensure it's a different object