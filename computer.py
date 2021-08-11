from enum import Enum
from typing import Any,Dict,List,Callable


ProgramCounter = int


class Operand(Enum):
    REGISTER = 1
    CONSTANT = 2
    ADDRESS = 4
    ANY = 7

    def __or__(self,other:Enum):
        return self.value | other.value
    def __ror__(self,other:Enum):
        return self.__or__(other)
    def __and__(self,other:int):
        return self.value & other
    def __rand__(self,other:int):
        return self.__and__(other)

class Operation:
    def __init__(self,identifier:Any,function:Callable[[list[str],Dict[str,Any],ProgramCounter],ProgramCounter],operands:List[Operand]):
        self.identifier = identifier
        self.function = function
        self.operands = operands

class Instruction:
    def __init__(self,operation:Operation,arguments:List[str]):
        self.operation = operation
        self.arguments = arguments
        assert(len(operation.operands) == len(arguments))

    def __call__(self,pc:ProgramCounter,regs:Dict[str,Any]):
        return self.operation.function(self.arguments,regs,pc)

    def __str__(self):
        return f'{self.operation.identifier} {" ".join(self.arguments)}'

class Computer:
    def __init__(self,registers:Dict[str,Any],initial_pc:ProgramCounter=0):
        self.pc = initial_pc
        self.regs = registers

    def execute_instruction(self,instruction:Instruction):
        self.pc = instruction(self.pc,self.regs)

    def execute(self,program:list[Instruction]):
        while 0 <= self.pc < len(program):
            self.execute_instruction(program[self.pc])

    def execute_with_profiler(self,program:list[Instruction],logging_condition:Callable[[ProgramCounter,Dict[str,Any]],bool]=None) -> Dict[int,int]:
        profile = {i:0 for i in range(len(program))}
        while 0 <= self.pc < len(program):
            profile[self.pc] += 1
            self.execute_instruction(program[self.pc])
            if logging_condition is not None and logging_condition(self.pc,self.regs):
                print(f'Program Counter: {self.pc}, Registers: {self.regs}')
        print('Program profile:',profile)