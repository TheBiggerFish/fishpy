"""Provides a class for calculating integer square roots"""

from typing import List


def _get_pairs(n: int):
    string = str(n)
    if len(string) % 2 != 0:
        string = '0' + string
    return [int(string[i:i+2]) for i in range(0, len(string), 2)]


def integer_square_root(n: int, precision: int) -> List[int]:
    """A function for calculating integer square roots"""
    #  https://en.wikipedia.org/wiki/Methods_of_computing_square_roots#Decimal_(base_10)

    value = []
    pairs = _get_pairs(n)

    c, p = 0, 0
    for i in range(precision):
        c = c*100 + 0 if i >= len(pairs) else pairs[i]
        x = 0
        while x * (20*p + x) <= c:
            x += 1
        x -= 1
        value.append(x)
        y = x * (20*p + x)
        p = p * 10 + x
        c -= y
    return value
