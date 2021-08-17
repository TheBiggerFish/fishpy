from typing import List
from sympy.ntheory.factor_ import totient
from math import prod 

# https://en.wikipedia.org/wiki/Modular_multiplicative_inverse#Using_Euler's_theorem
def modular_inverse(n:int,base:int) -> int:
    n **= totient(base) - 1
    n %= base
    return n

# https://crypto.stanford.edu/pbc/notes/numbertheory/crt.html
def chinese_remainder_theorem(a:List[int],m:List[int]) -> int:
    assert len(a) == len(m)

    M = prod(m)
    solution = 0
    for i in range(len(a)):
        b = M // m[i]
        b_inv = modular_inverse(b,m[i])
        solution += a[i] * b * b_inv
    return solution % M
