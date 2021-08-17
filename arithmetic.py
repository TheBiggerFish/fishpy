from typing import Callable, List
from fishpy.structures import Node


class Operation:
    def __init__(self,rep:str,func:Callable):
        self.rep = rep
        self.func = func

class GroupOperation(Operation):
    def __init__(self,open:str,close:str):
        super().__init__(open+close,lambda a:a)
        self.open = open
        self.close = close

ADDITION = Operation('+',lambda a,b: a+b)
SUBTRACTION = Operation('-',lambda a,b: a-b)
MULTIPLICATION = Operation('*',lambda a,b: a*b)
DIVISION = Operation('/',lambda a,b: a/b)
MODULUS = Operation('%',lambda a,b: a%b)
EXPONENTIATION = Operation('^',lambda a,b: a**b)
PARENTHESES = GroupOperation('(',')')


class OrderedOperation:
    def __init__(self,op:Operation,precedence:int=0):
        self.operation = op
        self.precedence = precedence

    def __lt__(self,other):
        return self.precedence < other.precedence

PEMDAS = [OrderedOperation(PARENTHESES,3),
          OrderedOperation(EXPONENTIATION,2),
          OrderedOperation(MULTIPLICATION,1),
          OrderedOperation(DIVISION,1),
          OrderedOperation(MODULUS,1),
          OrderedOperation(ADDITION,0),
          OrderedOperation(SUBTRACTION,0)]


class Expression(Node):
    def __init__(self,exp:str,order_of_operations:List[OrderedOperation]=PEMDAS):
        super().__init__(None,'',[])
        self._order_of_operations = order_of_operations
        self._str_exp = ''.join(exp.split())
        self._ops = {char:op.operation for op in order_of_operations for char in op.operation.rep}

        self._precedences = {}
        self._group_characters = set()
        for op in order_of_operations:
            if isinstance(op.operation,GroupOperation):
                self._group_characters |= set(op.operation.rep)
            else:
                if op.precedence not in self._precedences:
                    self._precedences[op.precedence] = set()
                self._precedences[op.precedence] |= set(op.operation.rep)

        self._generate()

    def __str__(self):
        if isinstance(self.value,int) or isinstance(self.value,float):
            return str(self.value)
        elif isinstance(self.value,GroupOperation):
            return self.value.open + str(self.children[0]) + self.value.close
        elif isinstance(self.value,Operation):
            return str(self.children[0]) + self.value.rep + str(self.children[1])

    def evaluate(self):
        if isinstance(self.value,int) or isinstance(self.value,float):
            return self.value
        elif isinstance(self.value,GroupOperation):
            return self.children[0].evaluate()
        elif isinstance(self.value,Operation):
            return self.value.func(self.children[0].evaluate(),self.children[1].evaluate())
    
    @staticmethod
    def find_matching_operator(exp:str,index:int,group_op:GroupOperation):
        if exp[index] == group_op.open:
            params = (1,index+1,len(exp),1)
        elif exp[index] == group_op.close:
            params = (-1,index-1,-1,-1)
        else:
            raise ValueError(f'Initial index {(index,exp[index])} provided does not match GroupOperation provided \'{group_op.rep}\'')

        count = params[0]
        for i in range(*params[1:]):
            if exp[i] == group_op.open:
                count += 1
            elif exp[i] == group_op.close:
                count -= 1
            if count == 0:
                return i
        return -1

    def _generate(self):
        if self._str_exp.isnumeric():
            self.value = int(self._str_exp)
            return

        for op in self._ops:
            op = self._ops[op]
            if isinstance(op,GroupOperation):
                if self._str_exp[0] == op.open:
                    if Expression.find_matching_operator(self._str_exp,0,op) == len(self._str_exp)-1:
                        self.value = op
                        child = Expression(self._str_exp[1:-1],self._order_of_operations)
                        self.add_child(child)
                        child.parent = self
                        return
                    break

        depth = 0
        for precedence in sorted(self._precedences.keys()):
            op_chars = self._precedences[precedence] | self._group_characters
            for i,char in enumerate(self._str_exp):
                if char in op_chars:
                    op = self._ops[char]
                    if isinstance(op,GroupOperation):
                        if char == op.open:
                            depth += 1
                        elif char == op.close:
                            depth -= 1
                        else:
                            raise Exception(f'Operation {char} not recognized')
                    elif depth == 0:
                        left = Expression(self._str_exp[:i],self._order_of_operations)
                        right = Expression(self._str_exp[i+1:],self._order_of_operations)
                        self.value = op
                        self.add_child(left)
                        left.parent = self
                        self.add_child(right)
                        right.parent = self
                        return
