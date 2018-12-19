# cython: language_level = 3
"""
Linking functions used in multigenic chromosomes.
"""
from operator import mul

def sum_linker(*args):
    return sum(args)

treduce = lambda op, lst, st: st if len(lst) == 0 else treduce(op, lst[1:], op(lst[0], st))

def multiply_linker(*args):
    return treduce(mul, args, 1)

def max_linker(*args):
    return max(args)

def argmax_linker(*args):
    return max(enumerate(args), key=lambda x: x[1])

def min_linker(*args):
    return min(args)

def argmin_linker(*args):
    return min(enumerate(args), key=lambda x: x[1])

def tuple_linker(*args):
    return tuple(args)

def list_linker(*args):
    return list(args)


