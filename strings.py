import string

LETTER_SET = set(string.ascii_letters)
LOWERCASE_SET = set(string.ascii_lowercase)
UPPERCASE_SET = set(string.ascii_uppercase)
DIGIT_SET = set(string.digits)
PUNCTUATION_SET = set(string.punctuation)
WHITESPACE_SET = set(string.whitespace)
ALPHANUMERIC_SET = LETTER_SET | DIGIT_SET

def levenshtein(a:str, b:str) -> int:
    if not len(a):
        return len(b)
    if not len(b):
        return len(a)
    if a[0] == b[0]:
        return levenshtein(a[1:],b[1:])
    return 1 + min(
        levenshtein(a[1:],b),
        levenshtein(a,b[1:]),
        levenshtein(a[1:],b[1:])
    )


def adjacent_strings(string:str,char_set:set=LETTER_SET,removal:bool=True,addition:bool=True,substitution:bool=False,transpositions:bool=False):
    rv = []
    if removal:
        for i in range(len(string)):
            rv += [string[:i] + string[i+1:]]
    if addition:
        for i in range(len(string)+1):
            for char in char_set:
                rv += [string[:i] + char + string[i:]]
    if substitution:
        for i in range(len(string)):
            for char in char_set:
                rv += [string[:i] + char + string[i+1:]]
    if transpositions:
        for i in range(len(string)):
            for j in range(i+1,len(string)):
                rv += [string[:i] + string[j] + string[i+1:j] + string[i] + string[j+1:]]
    return rv
