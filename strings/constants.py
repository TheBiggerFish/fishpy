"""This module provides a set of constants"""

from string import (ascii_letters, ascii_lowercase, ascii_uppercase, digits,
                    punctuation, whitespace)
from typing import Final, Set

LETTER_SET: Final[Set[str]] = set(ascii_letters)
LOWERCASE_SET: Final[Set[str]] = set(ascii_lowercase)
UPPERCASE_SET: Final[Set[str]] = set(ascii_uppercase)
DIGIT_SET: Final[Set[str]] = set(digits)
PUNCTUATION_SET: Final[Set[str]] = set(punctuation)
WHITESPACE_SET: Final[Set[str]] = set(whitespace)
ALPHANUMERIC_SET: Final[Set[str]] = LETTER_SET | DIGIT_SET
