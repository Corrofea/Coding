"""
>>> q
1
"""
from operator import mod
def quotient(n, d):
    """
    >>> q
    2
    """
    return mod(n, d)
q = quotient(101, 10)
