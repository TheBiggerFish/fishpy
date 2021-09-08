from math import gcd
from typing import Optional, Sequence, Union

class Fraction:
    def __init__(self,numer,denom=1):
        self.n = numer
        self.d = denom
    
    def is_proper(self) -> bool:
        return self.n < self.d

    def evaluate(self) -> bool:
        return self.n / self.d

    def reciprocal(self) -> 'Fraction':
        return Fraction(self.d,self.n)
    
    def add_int(self,num:int) -> 'Fraction':
        return Fraction(self.n + (num * self.d),self.d)

    def __mul__(self,other:'Fraction') -> 'Fraction':
        return Fraction(self.n*other.n,self.d*other.d)
    
    def __add__(self,other:'Fraction') -> 'Fraction':
        lcd = Fraction.lcd(self,other)
        self_n = self.n * (lcd // self.d)
        other_n = other.n * (lcd // other.d)
        return Fraction(self_n + other_n,lcd)

    def __str__(self) -> str:
        return str(self.n) + '/' + str(self.d)
    
    def __lt__(self,other:'Fraction') -> bool:
        return self.evaluate() < other.evaluate()

    def __gt__(self,other:'Fraction') -> bool:
        return self.evaluate() > other.evaluate()

    def __eq__(self,other:'Fraction') -> bool:
        return self.evaluate() == other.evaluate()

    @staticmethod
    def __lcm(a:int,b:int) -> int:
        return abs(a*b) // gcd(a,b)

    @staticmethod
    def lcd(f1:'Fraction',f2:'Fraction'):
        return Fraction.__lcm(f1.d,f2.d)

    def reduce(self) -> 'Fraction':
        div = gcd(self.n,self.d)
        return Fraction(self.n//div,self.d//div)

    def __hash__(self) -> int:
        if self.n >= self.d:
            return self.n * self.n + self.n + self.d
        else:
            return self.d * self.d + self.n

class ContinuedFraction:
    def __init__(self,addend:int=0,numer:int=0,denom:Optional['ContinuedFraction']=None):
        self.a = addend
        self.n = numer
        self.d = denom
        
    @staticmethod
    # Generate continued fraction using a continued fraction representation sequence.
    # The value x is used to generate the numerators of the continued fraction
    def gen_from_seq(seq:Sequence[int],x:int=2) -> 'ContinuedFraction':
        if len(seq) == 0:
            return ContinuedFraction(addend=0)

        frac = ContinuedFraction(addend=seq[-1])
        for num in reversed(seq[:-1]):
            if not isinstance(num,int):
                raise TypeError
            frac.d = frac.copy()
            frac.n = x-1
            frac.a = num
        return frac
    
    # Determines the representation sequence of a continued fraction
    def get_seq(self) -> Sequence[int]:
        seq = [self.a]
        frac = self.d
        while frac is not None:
            seq.append(frac.a)
            frac = frac.d
        return seq

    # Adds a continued fraction to the end of a continued fraction. 
    def append(self,frac:'ContinuedFraction') -> 'ContinuedFraction':
        recurse = self
        while recurse.d is not None:
            recurse = recurse.d
        recurse.d = frac
        return self

    def evaluate(self) -> float:
        if self.n == 0 or self.d is None:
            return float(self.a)
        return self.a + (self.n / self.d.evaluate())

    def reduce_fraction(self) -> Fraction:
        if self.n == 0 or self.d is None:
            return Fraction(self.a)
        return (Fraction(self.n) * self.d.reduce_fraction().reciprocal()).add_int(self.a)

    @staticmethod
    # Generate a continued fraction representation sequence of length l for a square root of number n
    def gen_sqrt_seq(n:int,l:int) -> Sequence[int]:
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
        return ContinuedFraction(addend=self.a,numer=self.n,denom=self.d)

    @property
    def a(self) -> int:
        return self.__a
        
    @property
    def n(self) -> int:
        return self.__n
    
    @property
    def d(self) -> 'ContinuedFraction':
        return self.__d

    @a.setter
    def a(self, a:int) -> None:
        if not isinstance(a,int) and not isinstance(a,float):
            raise TypeError
        self.__a = a

    @n.setter
    def n(self, n:int) -> None:
        if not isinstance(n,int) and not isinstance(n,float):
            raise TypeError
        self.__n = n

    @d.setter
    def d(self, d:'ContinuedFraction') -> None:
        self.__d = d