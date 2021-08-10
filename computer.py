from enum import Enum
from typing import Any,Dict,List,Callable


ProgramCounter = int


class Operand(Enum):
    ANY = 0
    REGISTER = 1
    CONSTANT = 2

class Operation:
    def __init__(self,identifier:Any,function:Callable[[list[str],Dict[str,Any],ProgramCounter],ProgramCounter],operands:List[Operand]):
        self.identifier = identifier
        self.function = function
        self.operands = operands

class Instruction:
    def __init__(self,operation:Operation,operands:List[str]):
        self.operation = operation
        self.operands = operands
        assert(len(operation.operands) == len(operands))

    def __call__(self,pc:ProgramCounter,regs:Dict[str,Any]):
        return self.operation.function(self.operands,regs,pc)

class Computer:
    def __init__(self,registers:Dict[str,Any],initial_pc:ProgramCounter=0):
        self.pc = initial_pc
        self.regs = registers

    def execute_instruction(self,instruction:Instruction):
        self.pc = instruction(self.pc,self.regs)

    def execute(self,program:list[Instruction]):
        if program is None:
            raise ValueError('Program must be provided to execute')
        while 0 <= self.pc < len(program):
            self.execute_instruction(program[self.pc])
