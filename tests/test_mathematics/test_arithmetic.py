import unittest

from fishpy.mathematics.arithmetic import (ADDITION, CURLY_BRACKETS, DIVISION,
                                           EXPONENTIATION, MODULUS,
                                           MULTIPLICATION, PARENTHESES, PEMDAS,
                                           SQUARE_BRACKETS, SUBTRACTION,
                                           EvaluationDirection, Expression,
                                           ExpressionNodeType, GroupOperation,
                                           Operation, OrderedOperation)


class TestOperation(unittest.TestCase):
    def setUp(self):
        def add(x, y): return x+y
        def sub(x, y): return x-y
        self.op1 = Operation('+', add)
        self.op2 = Operation('-', sub)

    def test_repr(self):
        self.assertEqual(repr(self.op1), 'Operation(\'+\')')
        self.assertEqual(repr(self.op2), 'Operation(\'-\')')


class TestGroupOperation(unittest.TestCase):
    def setUp(self):
        self.string1 = '()'
        self.string2 = '({)(})'
        self.string3 = '[[[[]]])'
        self.string4 = '((5+x)*3)'

    def test_find_matching_operator(self):
        self.assertEqual(
            PARENTHESES.find_matching_operator(self.string1, 0), 1)
        self.assertEqual(
            PARENTHESES.find_matching_operator(self.string2, 0), 2)
        self.assertEqual(
            SQUARE_BRACKETS.find_matching_operator(self.string3, 1), 6)
        self.assertEqual(
            SQUARE_BRACKETS.find_matching_operator(self.string3, 6), 1)
        self.assertEqual(
            CURLY_BRACKETS.find_matching_operator(self.string2, 4), 1)

        # Non-matching operator at index
        self.assertRaises(ValueError, PARENTHESES.find_matching_operator,
                          self.string2, 1)
        self.assertRaises(ValueError, SQUARE_BRACKETS.find_matching_operator,
                          self.string1, 1)

        # Operator unmatched in string
        self.assertRaises(ValueError, SQUARE_BRACKETS.find_matching_operator,
                          self.string3, 0)
        self.assertRaises(ValueError, PARENTHESES.find_matching_operator,
                          self.string3, 7)

    def test_is_around_string(self):
        self.assertTrue(PARENTHESES.is_around_string(self.string1))
        self.assertTrue(PARENTHESES.is_around_string(self.string4))
        self.assertFalse(PARENTHESES.is_around_string(self.string2))
        self.assertFalse(SQUARE_BRACKETS.is_around_string(self.string3))
        self.assertFalse(CURLY_BRACKETS.is_around_string(self.string2))

    def test_group_string(self):
        self.assertEqual(PARENTHESES.group_string(self.string1), '(())')
        self.assertEqual(PARENTHESES.group_string(
            '2+'+self.string4), '(2+((5+x)*3))')
        self.assertEqual(SQUARE_BRACKETS.group_string(
            self.string3), '[[[[[]]])]')
        self.assertEqual(CURLY_BRACKETS.group_string(self.string2), '{({)(})}')

    def test_repr(self):
        self.assertEqual(repr(PARENTHESES), 'GroupOperation(\'()\')')
        self.assertEqual(repr(SQUARE_BRACKETS), 'GroupOperation(\'[]\')')
        self.assertEqual(repr(CURLY_BRACKETS), 'GroupOperation(\'{}\')')


class TestOrderedOperation(unittest.TestCase):
    def setUp(self):
        self.op1 = OrderedOperation(ADDITION, precedence=4)
        self.op2 = OrderedOperation(SUBTRACTION, precedence=3)
        self.op3 = OrderedOperation(SQUARE_BRACKETS,
                                    OrderedOperation.GROUP_OPERATION_ORDER)
        self.op4 = OrderedOperation(MULTIPLICATION, precedence=1)

    def test_repr(self):
        self.assertEqual(repr(self.op1),
                         'OrderedOperation(Operation(\'+\'),precedence=4)')
        self.assertEqual(repr(self.op2),
                         'OrderedOperation(Operation(\'-\'),precedence=3)')
        self.assertEqual(repr(self.op3),
                         'OrderedOperation(GroupOperation(\'[]\'),precedence=Group)')
        self.assertEqual(repr(self.op4),
                         'OrderedOperation(Operation(\'*\'),precedence=1)')

    def test_lt(self):
        self.assertLess(self.op2, self.op1)
        self.assertLess(self.op4, self.op2)
        self.assertLess(self.op4, self.op3)
        self.assertGreater(self.op3, self.op1)
        self.assertGreater(self.op3, self.op2)
        self.assertGreater(self.op3, self.op4)


class TestExpression(unittest.TestCase):
    def setUp(self):
        self.string1 = '5-((5+18)*3)'
        self.string2 = '9+4+(7+3/8)+(2*(3*2)^2)'
        self.string3 = '[[[[]]])'
        self.string4 = '(1+2-3*4/5)^6'

    def test_evaluate(self):
        self.assertEqual(Expression(
            5, ExpressionNodeType.CONSTANT).evaluate(), 5)

        expr_const_3 = Expression(3, ExpressionNodeType.CONSTANT)
        expr_const_5 = Expression(5, ExpressionNodeType.CONSTANT)
        expr_add = Expression(ADDITION, ExpressionNodeType.OPERATION,
                              [expr_const_3, expr_const_5])
        self.assertEqual(expr_add.evaluate(), 8)

        expr_paren = Expression(
            PARENTHESES, ExpressionNodeType.GROUP, [expr_const_3])
        self.assertEqual(expr_paren.evaluate(), 3)

    def test_build_from_string(self):
        self.assertEqual(Expression.build_from_string(
            self.string1).evaluate(), -64)
        self.assertEqual(Expression.build_from_string(
            self.string2).evaluate(), 92.375)
        self.assertRaises(ValueError, Expression.build_from_string,
                          self.string3)
        self.assertAlmostEqual(Expression.build_from_string(
            self.string4).evaluate(), 0.046656)


class TestOrderOfOperations(unittest.TestCase):
    def setUp(self) -> None:
        self.order1 = PEMDAS
        self.order2 = [
            OrderedOperation(MULTIPLICATION, precedence=4),
            OrderedOperation(EXPONENTIATION, precedence=3),
            OrderedOperation(SUBTRACTION, precedence=2),
            OrderedOperation(ADDITION, precedence=1),
            OrderedOperation(PARENTHESES,
                             OrderedOperation.GROUP_OPERATION_ORDER)
        ]

        self.string1 = '5^2*2+5-18*3'
        self.string2 = '8*2^3+5-(1-2+3)*1^3'

    def test_evaluation(self):
        expr_1_1 = Expression.build_from_string(self.string1, self.order1)
        expr_1_2 = Expression.build_from_string(self.string1, self.order2)
        expr_2_1 = Expression.build_from_string(self.string2, self.order1)
        expr_2_2 = Expression.build_from_string(self.string2, self.order2)

        self.assertRaises(ValueError, Expression.build_from_string,
                          '1/2', self.order2)

        self.assertEqual(expr_1_1.evaluate(), 1)
        self.assertEqual(expr_1_2.evaluate(), 576)
        self.assertEqual(expr_2_1.evaluate(), 67)
        self.assertEqual(expr_2_2.evaluate(), 4093)
