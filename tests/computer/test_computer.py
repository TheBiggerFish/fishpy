import unittest
from typing import Any, Dict, List

from computer import Computer, Instruction, Operand, Operation, ProgramCounter


class TestInstructionMethods(unittest.TestCase):
    def setUp(self):
        def inc_func(arguments: List[str], registers: Dict[str, Any],
                     pc: ProgramCounter) -> ProgramCounter:
            registers[arguments[0]] += 1
            return pc+1

        inc = Operation('inc', inc_func, [Operand.REGISTER])
        self.Instruction = Instruction(inc, ['a'])
        self.registers = {'a': 0, 'b': 0}

    def test_call(self):
        self.assertEqual(self.Instruction(pc=12, regs=self.registers), 13)
        self.assertEqual(self.Instruction(pc=13, regs=self.registers), 14)
        self.assertEqual(self.registers['a'], 2)

    def test_str(self):
        self.assertEqual(str(self.Instruction), 'inc a')
        self.Instruction.arguments = ['b']
        self.assertEqual(str(self.Instruction), 'inc b')


class TestComputerMethods(unittest.TestCase):
    def setUp(self):
        def inc_func(arguments: List[str], registers: Dict[str, Any],
                     pc: ProgramCounter) -> ProgramCounter:
            registers[arguments[0]] += 1
            return pc+1

        inc = Operation('inc', inc_func, [Operand.REGISTER])
        self.program = [
            Instruction(inc, ['a']),
            Instruction(inc, ['a']),
            Instruction(inc, ['b']),
            Instruction(inc, ['a']),
        ]

        self.computer = Computer(registers={'a': 0, 'b': 0})

    def test_execute_instruction(self):
        self.computer.execute_instruction(self.program[0])
        self.assertEqual(self.computer.pc, 0)
        self.assertEqual(self.computer.regs['a'], 1)

        self.computer.execute_instruction(self.program[2])
        self.assertEqual(self.computer.pc, 0)
        self.assertEqual(self.computer.regs['b'], 1)

    def test_execute(self):
        self.computer.execute(self.program)
        self.assertEqual(self.computer.pc, 4)
        self.assertEqual(self.computer.regs['a'], 3)
        self.assertEqual(self.computer.regs['b'], 1)


if __name__ == '__main__':
    unittest.main()
