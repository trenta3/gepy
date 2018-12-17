"""
Linking functions used in multigenic chromosomes.
"""
from operator import mul

def sum_linker(*args):
    return sum(args)

def multiply_linker(*args):
    return reduce(mul, args, 1)

def max_linker(*args):
    return max(args)

def argmax_linker(*args):
    return max(enumerate(args), key=lambda x: x[1])

def min_linker(*args):
    return min(args)

def argmin_linker(*args):
    return min(enumerate(args), key=lambda x: x[1])
