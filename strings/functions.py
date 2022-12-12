"""
This module provides a collection of functions to be used in string
manipulation and processing
"""

from typing import Optional, Set

from .constants import LETTER_SET


def levenshtein(a: str, b: str) -> int:
    """Find the levenshtein distance between two strings"""

    if not len(a):
        return len(b)
    if not len(b):
        return len(a)
    if a[0] == b[0]:
        return levenshtein(a[1:], b[1:])
    return 1 + min(
        levenshtein(a[1:], b),
        levenshtein(a, b[1:]),
        levenshtein(a[1:], b[1:])
    )


def adjacent_strings(string: str, char_set: Optional[Set[str]] = None,
                     removal: bool = True, addition: bool = True,
                     substitution: bool = False, transpositions: bool = False):
    """
    Returns all strings which are one edit-distance from an initial string
    Optionally enable/disable character removal, addition, substitution, or transposition
    Specify a set of characters
    """

    if char_set is None:
        char_set = LETTER_SET
    rv = set()
    if removal:
        for i in range(len(string)):
            rv = rv.union([string[:i] + string[i+1:]])
    if addition:
        for i in range(len(string)+1):
            for char in char_set:
                rv = rv.union([string[:i] + char + string[i:]])
    if substitution:
        for i in range(len(string)):
            for char in char_set:
                rv = rv.union([string[:i] + char + string[i+1:]])
    if transpositions:
        for i, string_i in enumerate(string):
            for j in range(i+1, len(string)):
                rv = rv.union([string[:i] + string[j] +
                               string[i+1:j] + string_i + string[j+1:]])
    return rv
