"""
These classes are used in lexing and parsing arithmetic expressions
Supports arbitrary orders of operations
"""

from enum import Enum
from typing import Any, Callable, Dict, Final, List, Optional, Set, Union

from ..structures import Node


class Operation:
    """
        Class to represent arithmetic operations and the functions that they
        represent
    """

    def __init__(self, rep: str, func: Callable):
        self.rep = rep
        self.func = func

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}(\'{self.rep}\')'


class GroupOperation(Operation):
    """
        Class to represent arithmetic operations that group terms, such as
        like brackets and parentheses
    """

    def __init__(self, open_char: str, close_char: str):
        super().__init__(open_char+close_char, lambda a: a)
        self.open = open_char
        self.close = close_char

    def find_matching_operator(self, exp: str, index: int) -> int:
        """
            Provided an expression and the index of an operator, return the
            index of the matching operator
        """

        if exp[index] == self.open:
            params = (1, index+1, len(exp), 1)
        elif exp[index] == self.close:
            params = (-1, index-1, -1, -1)
        else:
            raise ValueError(f'Initial index {(index,exp[index])} provided'
                             'does not match GroupOperation')

        count = params[0]
        for i in range(*params[1:]):
            if exp[i] == self.open:
                count += 1
            elif exp[i] == self.close:
                count -= 1
            if count == 0:
                return i
        raise ValueError(f'Unmatched group operator at position {index}')

    def is_around_string(self, exp: str) -> bool:
        """
            Returns true if the surrounding Group Operator can be removing
            without causing syntax issues
        """

        if len(exp) < 2:
            return False
        if exp[0] == self.open and exp[-1] == self.close:
            return self.find_matching_operator(exp, 0) == len(exp)-1
        return False

    def group_string(self, nested: Any) -> str:
        """Stringify input and surround with group operator"""
        return self.open + str(nested) + self.close


ADDITION: Final[Operation] = Operation('+', lambda a, b: a+b)
SUBTRACTION: Final[Operation] = Operation('-', lambda a, b: a-b)
MULTIPLICATION: Final[Operation] = Operation('*', lambda a, b: a*b)
DIVISION: Final[Operation] = Operation('/', lambda a, b: a/b)
MODULUS: Final[Operation] = Operation('%', lambda a, b: a % b)
EXPONENTIATION: Final[Operation] = Operation('^', lambda a, b: a**b)
PARENTHESES: Final[GroupOperation] = GroupOperation('(', ')')
SQUARE_BRACKETS: Final[GroupOperation] = GroupOperation('[', ']')
CURLY_BRACKETS: Final[GroupOperation] = GroupOperation('{', '}')


class OrderedOperation:
    """
        Class to represent and compare operations that must be performed in
        order
    """

    GROUP_OPERATION_ORDER: Final[int] = -1

    def __init__(self, op: Operation, precedence: int = 0):
        self.operation = op
        self.precedence = precedence

    def __repr__(self) -> str:
        if isinstance(self.operation, GroupOperation):
            precedence = 'Group'
        else:
            precedence = self.precedence
        return f'{self.__class__.__name__}({self.operation!r},precedence={precedence})'

    def __lt__(self, other: 'OrderedOperation'):
        if isinstance(self.operation, GroupOperation):
            return False
        if isinstance(other.operation, GroupOperation):
            return True
        return self.precedence < other.precedence


# Default order of operations created with a list of OrderedOperations
PEMDAS: Final[List[OrderedOperation]] = [
    OrderedOperation(PARENTHESES, OrderedOperation.GROUP_OPERATION_ORDER),
    OrderedOperation(EXPONENTIATION, 2),
    OrderedOperation(MULTIPLICATION, 1),
    OrderedOperation(DIVISION, 1),
    OrderedOperation(MODULUS, 1),
    OrderedOperation(ADDITION, 0),
    OrderedOperation(SUBTRACTION, 0)
]


class ExpressionNodeType(Enum):
    """Enumeration of types of nodes in the expression tree"""
    NONE = 0
    CONSTANT = 1
    OPERATION = 2
    GROUP = 3


class EvaluationDirection(Enum):
    """Enumeration in direction of evaluation"""
    RIGHT_TO_LEFT = -1
    LEFT_TO_RIGHT = 1


class Expression(Node):
    """
        Class to represent, interpret, and evaluate arithmetic expressions
        using arbitrary operations
    """

    def __init__(self, value: Union[int, float, Operation],
                 node_type: ExpressionNodeType,
                 children: Optional[List['Expression']] = None,
                 parent: Optional['Expression'] = None):
        if children is None:
            children: List['Expression'] = []
        super().__init__(value, '', children, parent)
        self.node_type = node_type

    def __str__(self) -> str:
        if self.node_type == ExpressionNodeType.CONSTANT:
            return str(self.value)
        if self.node_type == ExpressionNodeType.GROUP:
            if isinstance(self.value, GroupOperation):
                return self.value.group_string(self.children[0])
            raise TypeError('ExpressionNodeType', self.node_type,
                            'does not match with value type', type(self.value))
        if self.node_type == ExpressionNodeType.OPERATION:
            if isinstance(self.value, Operation):
                return str(self.children[0]) + self.value.rep + \
                    str(self.children[1])
            raise TypeError('ExpressionNodeType', self.node_type,
                            'does not match with value type', type(self.value))
        return ''

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}(type={self.node_type.name},value={self.value})'

    def evaluate(self) -> Union[float, int]:
        """Evaluate and return the value of the expression"""
        self.children: List['Expression']
        if self.node_type == ExpressionNodeType.CONSTANT:
            return self.value
        if self.node_type == ExpressionNodeType.GROUP:
            return self.children[0].evaluate()
        if self.node_type == ExpressionNodeType.OPERATION:
            if isinstance(self.value, Operation):
                return self.value.func(self.children[0].evaluate(),
                                       self.children[1].evaluate())
            raise TypeError('ExpressionNodeType', self.node_type,
                            'does not match with value type', type(self.value))
        return 0

    @staticmethod
    def build_from_string(exp: str,
                          order_of_operations: Optional[List[OrderedOperation]] = None,
                          eval_dir: EvaluationDirection = EvaluationDirection.LEFT_TO_RIGHT):
        """
            Interpret an arithmetic expression string using a provided order
            of operations and evaluation direction. Returns the resulting
            Expression object
        """

        if order_of_operations is None:
            order_of_operations = PEMDAS

        str_exp = ''.join(exp.split())
        op_chars = {char: op.operation for op in order_of_operations
                    for char in op.operation.rep}
        group_characters = {char: op_chars[char] for char in op_chars
                            if isinstance(op_chars[char], GroupOperation)}
        precedences = {}
        for oper in order_of_operations:
            if oper.operation.rep[0] not in group_characters:
                if oper.precedence not in precedences:
                    precedences[oper.precedence] = set()
                precedences[oper.precedence] |= set(oper.operation.rep)

        return Expression._build_from_string_traverse(str_exp, op_chars,
                                                      group_characters,
                                                      precedences, eval_dir)

    @staticmethod
    def _build_from_string_traverse(exp: str, op_chars: Dict[str, Operation],
                                    group_chars: Dict[str, GroupOperation],
                                    precedences: Dict[int, Set[str]],
                                    eval_dir: EvaluationDirection):
        # Constant Type
        if (num := Expression._str_is_float_or_int(exp)) is not None:
            return Expression(num, ExpressionNodeType.CONSTANT, [])

        if len(exp) < 3:
            raise ValueError(f'Expression string not traversible: "{exp}"')

        # Group Type
        if exp[0] in group_chars and group_chars[exp[0]].is_around_string(exp):
            char = exp[0]
            child: Expression = Expression._build_from_string_traverse(
                exp[1:-1], op_chars, group_chars, precedences, eval_dir
            )
            parent = Expression(group_chars[char],
                                ExpressionNodeType.GROUP, [child])
            child.parent = parent
            return parent

        if eval_dir == EvaluationDirection.RIGHT_TO_LEFT:
            eval_slice = slice(0, len(exp)-1, 1)
        elif eval_dir == EvaluationDirection.LEFT_TO_RIGHT:
            eval_slice = slice(len(exp)-1, 0, -1)
        else:
            raise ValueError(
                f'Invalid value for EvaluationDirection: {eval_dir}')

        for pre in sorted(precedences.keys()):
            i = eval_slice.start
            while eval_slice.start <= i <= eval_slice.stop or \
                    eval_slice.stop <= i <= eval_slice.start:
                char = exp[i]
                if char in group_chars:
                    i = group_chars[char].find_matching_operator(exp, i)
                elif char in precedences[pre]:
                    left_child: Expression = Expression._build_from_string_traverse(
                        exp[:i], op_chars, group_chars, precedences, eval_dir
                    )
                    right_child: Expression = Expression._build_from_string_traverse(
                        exp[i+1:], op_chars, group_chars, precedences, eval_dir
                    )
                    parent = Expression(op_chars[char],
                                        ExpressionNodeType.OPERATION,
                                        [left_child, right_child])
                    left_child.parent = parent
                    right_child.parent = parent
                    return parent
                i += eval_slice.step
        raise ValueError(f'Expression string not traversible {exp}')

    @staticmethod
    def _str_is_float_or_int(exp: str) -> Union[int, float, None]:
        if exp.isnumeric():
            return int(exp)
        try:
            return float(exp)
        except ValueError:
            return None
