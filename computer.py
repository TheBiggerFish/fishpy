"""Virtual machine configurable to simple programming languages"""

from enum import IntFlag
from typing import Any, Callable, Dict, List, NewType

ProgramCounter = NewType('ProgramCounter', int)
RegisterDict = Dict[str, Any]
ArgList = List[str]
OpFunc = Callable[[ArgList, RegisterDict, ProgramCounter], ProgramCounter]
StateCondition = Callable[[ProgramCounter, RegisterDict], bool]


class Operand(IntFlag):
    """Enumeration of operands to be used in operations"""

    REGISTER = 1
    CONSTANT = 2
    ADDRESS = 4
    ANY = 7


class Operation:
    """Class representing program operations"""

    def __init__(self, identifier: Any, function: OpFunc, operands: List[Operand]):
        self.identifier = identifier
        self.function = function
        self.operands = operands


class Instruction:
    """Class representing individual program instructions"""

    def __init__(self, operation: Operation, arguments: ArgList):
        self.operation = operation
        self.arguments = arguments
        assert len(operation.operands) == len(arguments)

    def __call__(self, pc: ProgramCounter, regs: RegisterDict):
        return self.operation.function(self.arguments, regs, pc)

    def __str__(self):
        return f'{self.operation.identifier} {" ".join(self.arguments)}'

    def __repr__(self):
        return f'Instruction("{self}")'


class Computer:
    """Class used to execute programs"""

    def __init__(self, registers: RegisterDict, initial_pc: ProgramCounter = 0):
        self.pc = initial_pc
        self.regs = registers

    def __repr__(self) -> str:
        return f'Computer(pc:{self.pc},registers:{self.regs})'

    def execute_instruction(self, instruction: Instruction) -> ProgramCounter:
        """Execute a single instruction on the computer"""
        return instruction(self.pc, self.regs)

    def execute(self, program: List[Instruction]):
        """Execute a list of instructions until the PC falls outside of range"""
        while 0 <= self.pc < len(program):
            self.pc = self.execute_instruction(program[self.pc])

    def execute_with_profiler(self, program: List[Instruction],
                              logging_condition: StateCondition = None):
        """
        Execute a list of instructions until the counter falls outside of range
        Count the number of times each instruction is executed
        """

        profile = {i: 0 for i in range(len(program))}
        while 0 <= self.pc < len(program):
            profile[self.pc] += 1
            self.pc = self.execute_instruction(program[self.pc])
            if logging_condition is not None and logging_condition(self.pc, self.regs):
                print(f'Program Counter: {self.pc}, Registers: {self.regs}')
        print('Program profile:', profile)
