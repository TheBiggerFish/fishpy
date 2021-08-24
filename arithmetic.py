from typing import Any, Callable, Dict, List, Set, Tuple, Type, Union
from fishpy.structures import Node,Enum


class Operation:
    def __init__(self,rep:str,func:Callable):
        self.rep = rep
        self.func = func

class GroupOperation(Operation):
    def __init__(self,open:str,close:str):
        super().__init__(open+close,lambda a:a)
        self.open = open
        self.close = close    
        
    def find_matching_operator(self,exp:str,index:int) -> int:
        if exp[index] == self.open:
            params = (1,index+1,len(exp),1)
        elif exp[index] == self.close:
            params = (-1,index-1,-1,-1)
        else:
            raise ValueError(f'Initial index {(index,exp[index])} provided does not match GroupOperation')

        count = params[0]
        for i in range(*params[1:]):
            if exp[i] == self.open:
                count += 1
            elif exp[i] == self.close:
                count -= 1
            if count == 0:
                return i
        return -1
    
    def is_around_string(self,exp:str) -> bool:
        if len(exp) < 2:
            return False
        if exp[0] == self.open and exp[-1] == self.close:
            return self.find_matching_operator(exp,0) == len(exp)-1
        return False
    
    def group_string(self,nested:Any) -> str:
        return self.open + str(nested) + self.close

ADDITION = Operation('+',lambda a,b: a+b)
SUBTRACTION = Operation('-',lambda a,b: a-b)
MULTIPLICATION = Operation('*',lambda a,b: a*b)
DIVISION = Operation('/',lambda a,b: a/b)
MODULUS = Operation('%',lambda a,b: a%b)
EXPONENTIATION = Operation('^',lambda a,b: a**b)
PARENTHESES = GroupOperation('(',')')


class OrderedOperation:
    GROUP_OPERATION_ORDER = -1
    
    def __init__(self,op:Operation,precedence:int=0):
        self.operation = op
        self.precedence = precedence

    def __lt__(self,other):
        if isinstance(self,GroupOperation):
            return False
        elif isinstance(other,GroupOperation):
            return True
        return self.precedence < other.precedence

PEMDAS = [OrderedOperation(PARENTHESES,OrderedOperation.GROUP_OPERATION_ORDER),
          OrderedOperation(EXPONENTIATION,2),
          OrderedOperation(MULTIPLICATION,1),
          OrderedOperation(DIVISION,1),
          OrderedOperation(MODULUS,1),
          OrderedOperation(ADDITION,0),
          OrderedOperation(SUBTRACTION,0)]

class ExpressionNodeType(Enum):
    NONE = 0
    CONSTANT = 1
    OPERATION = 2
    GROUP = 3

class EvaluationDirection(Enum):
    RIGHT_TO_LEFT = -1
    LEFT_TO_RIGHT = 1
    

class Expression(Node):
    def __init__(self,value:Union[int,float,Operation],node_type:ExpressionNodeType,children:List,parent=None):
        super().__init__(value,'',children,parent)
        self.node_type = node_type
        
    def __str__(self):
        if self.node_type == ExpressionNodeType.CONSTANT:
            return str(self.value)
        elif self.node_type == ExpressionNodeType.GROUP:
            if isinstance(self.value,GroupOperation):
                return self.value.group_string(self.children[0])
            else:
                raise TypeError('ExpressionNodeType',self.node_type,'does not match with value type',type(self.value))
        elif self.node_type == ExpressionNodeType.OPERATION:
            if isinstance(self.value,Operation):
                return str(self.children[0]) + self.value.rep + str(self.children[1])
            else:
                raise TypeError('ExpressionNodeType',self.node_type,'does not match with value type',type(self.value))
        return ''

    def evaluate(self) -> Union[float,int]:
        if self.node_type == ExpressionNodeType.CONSTANT:
            return self.value
        elif self.node_type == ExpressionNodeType.GROUP:
            return self.children[0].evaluate()
        elif self.node_type == ExpressionNodeType.OPERATION:
            if isinstance(self.value,Operation):
                return self.value.func(self.children[0].evaluate(),self.children[1].evaluate())
            else:
                raise TypeError('ExpressionNodeType',self.node_type,'does not match with value type',type(self.value))
        return 0


    @staticmethod
    def build_from_string(exp:str,order_of_operations:List[OrderedOperation]=PEMDAS,eval_dir:EvaluationDirection=EvaluationDirection.LEFT_TO_RIGHT):
        str_exp = ''.join(exp.split())
        op_chars = {char:op.operation for op in order_of_operations for char in op.operation.rep}
        group_characters = {char:op_chars[char] for char in op_chars if isinstance(op_chars[char],GroupOperation)}
        precedences = {}
        for op in order_of_operations:
            if op.operation.rep[0] not in group_characters:
                if op.precedence not in precedences:
                    precedences[op.precedence] = set()
                precedences[op.precedence] |= set(op.operation.rep)
                
        exp_obj = Expression._build_from_string_traverse(str_exp,op_chars,group_characters,precedences,eval_dir)
        exp_obj._analyze()
        return exp_obj
    
    def _analyze(self):
        pass
    
    @staticmethod
    def _build_from_string_traverse(exp:str,op_chars:Dict[str,Operation],group_chars:Dict[str,GroupOperation],precedences:Dict[int,Set[str]],eval_dir:EvaluationDirection):
        # Constant Type
        if (foi := Expression._str_is_float_or_int(exp))[0]:
            return Expression(foi[1], ExpressionNodeType.CONSTANT,[])
        
        if len(exp) < 3:
            raise ValueError(f'Expression string not traversible {exp}')
        
        # Group Type
        for char in group_chars:
            if group_chars[char].is_around_string(exp):
                child = Expression._build_from_string_traverse(exp[1:-1],op_chars,group_chars,precedences,eval_dir)
                parent = Expression(group_chars[char],ExpressionNodeType.GROUP,[child])
                child.parent = parent
                return parent
        
        if eval_dir == EvaluationDirection.RIGHT_TO_LEFT:
            start,end,step = 0,len(exp)-1,1
        elif eval_dir == EvaluationDirection.LEFT_TO_RIGHT:
            start,end,step = len(exp)-1,0,-1
        else:
            raise ValueError(f'Invalid value for EvaluationDirection: {eval_dir}')

        for pre in sorted(precedences.keys()):
            i = start
            while start <= i <= end or end <= i <= start:
                char = exp[i]
                if char in group_chars:
                    i = group_chars[char].find_matching_operator(exp,i)
                elif char in precedences[pre]:
                    left = Expression._build_from_string_traverse(exp[:i],op_chars,group_chars,precedences,eval_dir)
                    right = Expression._build_from_string_traverse(exp[i+1:],op_chars,group_chars,precedences,eval_dir)
                    parent = Expression(op_chars[char],ExpressionNodeType.OPERATION,[left,right])
                    left.parent = parent
                    right.parent = parent
                    return parent
                i += step
        raise ValueError(f'Expression string not traversible {exp}')
        
    @staticmethod
    def _str_is_float_or_int(exp:str) -> Tuple[bool,Union[int,float,None]]:
        if exp.isnumeric():
            return True,int(exp)
        try:
            return True,float(exp)
        except:
            return False,None

