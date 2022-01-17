"""Structures to be used in evaluating fractions and continued fractions"""

#pylint: disable=invalid-name

from math import gcd
from typing import Optional, Sequence


class Fraction:
    """Class to be used in storing and evaluating fractions"""

    def __init__(self, numer: int, denom: int = 1):
        self.n = numer
        self.d = denom

    def is_proper(self) -> bool:
        """Predicate method that returns whether the function is proper"""
        return self.n < self.d

    def evaluate(self) -> float:
        """Return the actual value of of the fraction"""
        return self.n / self.d

    def reciprocal(self) -> 'Fraction':
        """Return the reciprocal fraction of self"""
        return Fraction(self.d, self.n)

    def add_int(self, num: int) -> 'Fraction':
        """Add an integer value to the fraction"""
        return Fraction(self.n + (num * self.d), self.d)

    def reduce(self) -> 'Fraction':
        """Reduce the fraction to the lowest equivalent value"""
        div = gcd(self.n, self.d)
        return Fraction(self.n//div, self.d//div)

    @staticmethod
    def _lcd(f1: 'Fraction', f2: 'Fraction'):
        return Fraction._lcm(f1.d, f2.d)

    @staticmethod
    def _lcm(a: int, b: int) -> int:
        return abs(a*b) // gcd(a, b)

    def __mul__(self, other: 'Fraction') -> 'Fraction':
        return Fraction(self.n*other.n, self.d*other.d)

    def __add__(self, other: 'Fraction') -> 'Fraction':
        lcd = Fraction._lcd(self, other)
        self_n = self.n * (lcd // self.d)
        other_n = other.n * (lcd // other.d)
        return Fraction(self_n + other_n, lcd)

    def __str__(self) -> str:
        return str(self.n) + '/' + str(self.d)

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}(n={self.n},d={self.d})'

    def __lt__(self, other: 'Fraction') -> bool:
        return self.evaluate() < other.evaluate()

    def __gt__(self, other: 'Fraction') -> bool:
        return self.evaluate() > other.evaluate()

    def __eq__(self, other: 'Fraction') -> bool:
        return self.evaluate() == other.evaluate()

    def __hash__(self) -> int:
        if self.n >= self.d:
            return self.n * self.n + self.n + self.d
        return self.d * self.d + self.n


class ContinuedFraction:
    """Class for storing continued fractions"""

    def __init__(self, addend: int = 0, numer: int = 0,
                 denom: Optional['ContinuedFraction'] = None):
        self.a = addend
        self.n = numer
        self.d = denom

    def __repr__(self) -> str:
        denom = self.d.__class__.__name__ if self.d is not None else None
        return (f'{self.__class__.__name__}(addend={self.a},'
                f'numerator={self.n},denominator={denom})')

    @staticmethod
    def gen_from_seq(seq: Sequence[int], x: int = 2) -> 'ContinuedFraction':
        """
        Generate a continued fraction from a sequence of integers
        The value x is used to generate the numerators of the continued fraction
        """

        if len(seq) == 0:
            return ContinuedFraction(addend=0)

        frac = ContinuedFraction(addend=seq[-1])
        for num in reversed(seq[:-1]):
            if not isinstance(num, int):
                raise TypeError
            frac.d = frac.copy()
            frac.n = x-1
            frac.a = num
        return frac

    def get_seq(self) -> Sequence[int]:
        """Returns the sequence of integers that represents a continued fraction"""

        seq = [self.a]
        frac = self.d
        while frac is not None:
            seq.append(frac.a)
            frac = frac.d
        return seq

    def append(self, frac: 'ContinuedFraction') -> 'ContinuedFraction':
        """Append continued fraction to the last continued fraction"""

        recurse = self
        while recurse.d is not None:
            recurse = recurse.d
        recurse.d = frac
        return self

    def evaluate(self) -> float:
        """Recursively determine the value of the continued fraction"""

        if self.n == 0 or self.d is None:
            return float(self.a)
        return self.a + (self.n / self.d.evaluate())

    def reduce_fraction(self) -> Fraction:
        """Recursively evaluate the continued fraction to find a representative fraction"""
        if self.n == 0 or self.d is None:
            return Fraction(self.a)
        sub_fraction = Fraction(self.n) * self.d.reduce_fraction().reciprocal()
        return sub_fraction.add_int(self.a)

    @staticmethod
    def gen_sqrt_seq(n: int, l: int) -> Sequence[int]:
        """
        Generate a continued fraction representation sequence of length l for
        a square root of number n
        """

        if (n**0.5).is_integer():
            return [n**0.5]
        m = 0
        d = 1
        a = int(n**0.5)
        seq = [a]
        while len(seq) < l:
            m = d * a - m
            d = (n - (m**2)) // d
            a = int(((n**0.5) + m) // d)
            seq.append(a)
        return seq

    def copy(self) -> 'ContinuedFraction':
        """Returns a shallow copy of self"""
        return ContinuedFraction(addend=self.a, numer=self.n, denom=self.d)

    @property
    def a(self) -> int:
        """Represents the addend of the continued fraction"""
        return self.__a

    @property
    def n(self) -> int:
        """Represents the numerator of the continued fraction"""
        return self.__n

    @property
    def d(self) -> 'ContinuedFraction':
        """
        Represents the denominator of the continued fraction,
        another continued fraction
        """
        return self.__d

    @a.setter
    def a(self, a: int) -> None:
        if not isinstance(a, int) and not isinstance(a, float):
            raise TypeError
        self.__a = a

    @n.setter
    def n(self, n: int) -> None:
        if not isinstance(n, int) and not isinstance(n, float):
            raise TypeError
        self.__n = n

    @d.setter
    def d(self, d: 'ContinuedFraction') -> None:
        self.__d = d
