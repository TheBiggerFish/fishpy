"""
This module provides a set of functions related to multisets.
"""

from multiset import Multiset

from .primes import is_prime


def multiset_prime_factors(n, primes=None):
    """Find the smallest subset of prime factors using multisets"""

    # If n is prime, return a multiset containing only n
    if (primes is None and is_prime(n)) or (primes is not None and n in primes):
        return Multiset([n])

    # Find the first divisor of n, add the prime multisets containing factors of the divisors
    for i in range(2, int(n**0.5)+1):
        if n % i == 0:
            return multiset_prime_factors(i) + multiset_prime_factors(n//i)
    return Multiset([])

# def multiset_factors(n,primes=None):
#     f = Multiset()
#     for i in range(1,int(n**0.5)+1):
#         if n%i == 0:
#             f.add(i,n//i)
#             f.add(n//i,i)
#     return f
