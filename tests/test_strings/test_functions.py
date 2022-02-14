
import unittest

from fishpy.strings import adjacent_strings, levenshtein


class TestLevenshtein(unittest.TestCase):
    def setUp(self):
        self.string_1 = 'orange'
        self.string_2 = 'apple'
        self.string_3 = 'banana'
        self.string_4 = 'bananas'

    def test_execution(self):
        self.assertEqual(levenshtein(self.string_1, self.string_1), 0)
        self.assertEqual(levenshtein(self.string_1, self.string_2), 5)
        self.assertEqual(levenshtein(self.string_3, self.string_4), 1)


class TestAdjacentStrings(unittest.TestCase):
    def setUp(self):
        self.string_1 = ''
        self.string_2 = 'a'
        self.string_3 = 'ab'
        self.string_4 = 'abc'

        self.char_set_1 = set('abc')
        self.char_set_2 = set('abcdefghij')

    def test_removal_and_addition(self):
        self.assertEqual(len(adjacent_strings(self.string_1)), 52)
        self.assertEqual(len(adjacent_strings(self.string_2)), 104)
        self.assertEqual(len(adjacent_strings(self.string_3)), 156)
        self.assertEqual(len(adjacent_strings(self.string_4)), 208)

    def test_custom_char_set(self):
        self.assertEqual(len(adjacent_strings(self.string_1,
                                              self.char_set_1)), 3)
        self.assertEqual(len(adjacent_strings(self.string_4,
                                              self.char_set_1)), 12)
        self.assertEqual(len(adjacent_strings(self.string_1,
                                              self.char_set_2)), 10)
        self.assertEqual(len(adjacent_strings(self.string_4,
                                              self.char_set_2)), 40)

    def test_substitution(self):
        self.assertEqual(len(adjacent_strings(self.string_1,
                                              substitution=True)), 52)
        self.assertEqual(len(adjacent_strings(self.string_2,
                                              substitution=True)), 156)
        self.assertEqual(len(adjacent_strings(self.string_3,
                                              substitution=True)), 259)
        self.assertEqual(len(adjacent_strings(self.string_4,
                                              substitution=True)), 362)
        self.assertEqual(len(adjacent_strings(self.string_4, self.char_set_2,
                                              substitution=True)), 68)
