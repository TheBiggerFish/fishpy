import unittest

from fishpy.pathfinding.grid import Grid, Cell
from fishpy.geometry import LatticePoint


class TestGrid(unittest.TestCase):
    def setUp(self):
        self.empty_pathfinding_grid = Grid.blank(LatticePoint(8, 5))
        self.string_grid = Grid.from_list_of_iterables(['ABC','DEF','GHI'])
        self.numeric_grid = Grid.from_list_of_iterables([[1,2,3],[4,5,6],[7,8,9]])
        self.empty_numeric_grid = Grid.blank(LatticePoint(4, 4), default_value=0)
        self.offset_grid = Grid.from_iterable_of_cells([Cell(-1,-1, 'X'), Cell(0,0,'Y'), Cell(1,1,'Z')])
        self.zero_grid = Grid([])

    def test_get_item(self):
        # Test getting item from aligned grid
        self.assertEqual(self.string_grid[LatticePoint(0, 0)], 'A')

        # Test getting item from out-of-bounds in aligned grid
        self.assertRaises(KeyError, self.empty_numeric_grid.__getitem__, LatticePoint(-1, -1))

        # Test getting item from offset grid
        self.assertEqual(self.offset_grid[LatticePoint(-1, -1)], 'X')

        # Test getting item from out-of-bounds in offset grid
        self.assertRaises(KeyError, self.offset_grid.__getitem__, LatticePoint(-2, -2))

    def test_set_item(self):
        # Test setting item in aligned grid
        self.string_grid[LatticePoint(1, 1)] = 'Z'
        self.assertEqual(self.string_grid[LatticePoint(1, 1)], 'Z')

    def test_value_positions(self):
        positions = self.string_grid.value_positions('E')
        self.assertEqual(positions['E'], [LatticePoint(1, 1)])

        positions = self.empty_numeric_grid.value_positions([0])
        self.assertEqual(len(positions[0]), 16)  # 4x4 grid, all zeros

    def test_from_list_of_iterables(self):
        self.assertEqual(self.string_grid[LatticePoint(2, 2)], 'I')
        self.assertEqual(self.numeric_grid[LatticePoint(0, 2)], 7)

    def test_from_iterable_of_cells(self):
        self.assertEqual(self.offset_grid[LatticePoint(-1, -1)], 'X')
        self.assertEqual(self.offset_grid[LatticePoint(0, 0)], 'Y')
        self.assertEqual(self.offset_grid[LatticePoint(1, 1)], 'Z')
        self.assertEqual(self.offset_grid[LatticePoint(0, 1)], '.')
        self.assertRaises(KeyError, self.offset_grid.__getitem__, LatticePoint(2,0))

    def test_blank(self):
        self.assertEqual(self.empty_numeric_grid.size, LatticePoint(4, 4))
        self.assertEqual(self.empty_numeric_grid.offset, LatticePoint(0, 0))
        self.assertEqual(len(self.empty_numeric_grid.value_positions([0])[0]), 16)

    def test_width(self):
        self.assertEqual(self.empty_pathfinding_grid.width, 8)
        self.assertEqual(self.string_grid.width, 3)
        self.assertEqual(self.offset_grid.width, 3)
        self.assertEqual(self.zero_grid.width, 0)

    def test_height(self):
        self.assertEqual(self.empty_pathfinding_grid.height, 5)
        self.assertEqual(self.string_grid.height, 3)
        self.assertEqual(self.offset_grid.height, 3)
        self.assertEqual(self.zero_grid.height, 0)

    def test_size(self):
        self.assertEqual(self.empty_pathfinding_grid.size, LatticePoint(8, 5))
        self.assertEqual(self.string_grid.size, LatticePoint(3, 3))
        self.assertEqual(self.offset_grid.size, LatticePoint(3, 3))
        self.assertEqual(self.zero_grid.size, LatticePoint(0, 0))

    def test_offset(self):
        self.assertEqual(self.empty_pathfinding_grid.offset, LatticePoint(0, 0))
        self.assertEqual(self.string_grid.offset, LatticePoint(0, 0))
        self.assertEqual(self.offset_grid.offset, LatticePoint(-1, -1))
        self.assertEqual(self.zero_grid.offset, LatticePoint(0, 0))

    def test_bounds(self):
        self.assertEqual((LatticePoint(0, 0), LatticePoint(8, 5)), self.empty_pathfinding_grid.bounds)
        self.assertEqual((LatticePoint(0, 0), LatticePoint(3, 3)), self.string_grid.bounds)
        self.assertEqual((LatticePoint(-1, -1), LatticePoint(2, 2)), self.offset_grid.bounds)
        self.assertEqual((LatticePoint(0, 0), LatticePoint(0, 0)), self.zero_grid.bounds)

    def test_copy(self):
        grid_copy = self.string_grid.copy()
        self.assertEqual(grid_copy.size, self.string_grid.size)
        self.assertEqual(grid_copy.offset, self.string_grid.offset)
        self.assertEqual(grid_copy[LatticePoint(1, 1)], self.string_grid[LatticePoint(1, 1)])
        grid_copy[LatticePoint(1, 1)] = 'Z'
        self.assertNotEqual(grid_copy[LatticePoint(1, 1)], self.string_grid[LatticePoint(1, 1)])

    def test_conditional_update(self):
        def checkerboard(point: LatticePoint) -> str:
            return 'X' if (point.x + point.y) % 2 == 0 else 'O'
        checker_grid = self.empty_pathfinding_grid.conditional_update(checkerboard)
        self.assertEqual(checker_grid.size, self.empty_pathfinding_grid.size)
        self.assertEqual(checker_grid.offset, self.empty_pathfinding_grid.offset)
        for y in range(self.empty_pathfinding_grid.height):
            for x in range(self.empty_pathfinding_grid.width):
                expected = checkerboard(LatticePoint(x, y))
                actual = checker_grid[LatticePoint(x, y)]
                self.assertEqual(expected, actual)
                self.assertEqual('.', self.empty_pathfinding_grid[LatticePoint(x, y)])  # Original grid unchanged


    def test_draw_search(self):
        pass

    def test_overlay(self):
        pass

    def test_to_string(self):
        pass

    def test_subgrid(self):
        pass

    def test_shift(self):
        pass

    def test_flood_fill(self):
        pass

    def test_draw_line(self):
        pass

    def test_row(self):
        pass

    def test_col(self):
        pass