"""Functions related to modular arithmetic"""

from math import prod
from typing import List

from sympy.ntheory.factor_ import totient


# https://en.wikipedia.org/wiki/Modular_multiplicative_inverse#Using_Euler's_theorem
def modular_inverse(n:int,base:int) -> int:
    """Returns the modular inverse of n in base"""
    n **= totient(base) - 1
    n %= base
    return n

# https://crypto.stanford.edu/pbc/notes/numbertheory/crt.html
def chinese_remainder_theorem(a:List[int],m:List[int]) -> int:
    """Performs the chinese remainder theorem on recieved lists"""

    if len(a) != len(m):
        raise ValueError('Length of a must match length of m')

    M = prod(m)
    solution = 0
    for i,m_i in enumerate(a):
        b = M // m_i
        b_inv = modular_inverse(b,m_i)
        solution += a[i] * b * b_inv
    return solution % M
