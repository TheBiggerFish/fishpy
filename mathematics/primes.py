"""
This module provides a set of functions related to prime numbers.
"""

from math import gcd
from typing import Set

from sympy.ntheory.factor_ import totient


def is_prime(n:int) -> bool:
    """Iteratively check every possible divisor to determine if n is prime"""

    if n in (2,3):
        return True
    if n % 2 == 0 or n % 3 == 0 or n <= 1:
        return False
    for divisor in range(6, min(int(n**0.5) + 6,n-1), 6):
        if n % (divisor - 1) == 0 or n % (divisor + 1) == 0:
            return False
    return True

def _witness_test(n:int, d:int, witness:int, exp:int) -> bool:
    for e in range(exp):
        result = 1
        for _ in range(d*(2**e)):
            result *= witness
            result %= n
        if result in (1,n-1):
            return True
    return False

def miller_rabin(n:int) -> bool:
    """Perform the Miller-Rabin test for primality to determine if n is prime"""

    if n == 2:
        return True
    if n % 2 == 0:
        return False

    witnesses = (2,3,5,7,11)

    d = n-1
    exp = 0
    while d % 2 == 0:
        d //= 2
        exp += 1

    for a in witnesses:
        if a == n:
            return True
        if not _witness_test(n,d,a,exp):
            return False
    return True

def factors(n:int) -> Set[int]:
    """Iteratively check every possible divisor to find the factors of n"""

    f = set()
    for i in range(1,int(n**0.5)+1):
        if n%i == 0:
            f.add(i)
            f.add(n//i)
    return f

def prime_factors(n:int) -> Set[int]:
    """Iteratively check every possible divisor to find prime factors of n"""

    f = set()
    if n % 2 == 0:
        f.add(2)
        while n % 2 == 0:
            n //= 2

    for i in range(3,int(n**0.5),2):
        if n % i == 0:
            f.add(i)
            while n % i == 0:
                n //= i
    if n > 1:
        f.add(n)
    return f

def sieve(max_:int) -> Set[int]:
    """Use Eratosthenes' sieve to find all prime numbers smaller than max_"""

    composite = set()
    for i in range(2,int(max_**0.5)+2):
        if i in composite:
            continue
        for j in range(i**2,max_,i):
            composite.add(j)
    return set(range(2,max_)).difference(composite)

def are_coprime(n1:int,n2:int) -> bool:
    """Predicate function to determine if 2 numbers are coprime"""

    if n1 % n2 == 0 or n2 % n1 == 0:
        return False
    return gcd(n1,n2) == 0

# https://math.stackexchange.com/questions/1854197/calculate-the-number-of-integers-in-a-given-interval-that-are-coprime-to-a-given
def range_totient(n:int,max_:int,min_:int=2) -> int:
    """
    Calculate the count of numbers in an interval which are coprime to n
    """

    full_range = int(max_-min_-((max_-min_)%n))
    rt = int(round(totient(n)/n * full_range,12))
    new_min = min_ + full_range + 1
    for i in range(new_min,max_+1):
        if are_coprime(i,n):
            rt += 1
    return rt
