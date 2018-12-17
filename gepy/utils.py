from random import random
from math import floor
from inspect import getargspec

def arity(fn):
    """
    Function that returns the arity of a function.
    """
    # return fn.func_code.co_argcount
    return len(getargspec(fn)[0])

def list_choose_rand(fromlist, num):
    """
    Select 'num' random elements from the list.
    """
    list_len = len(fromlist)
    return [fromlist[floor(random() * list_len)] for i in range(num)]

def choose_rand(lst):
    return lst[floor(random() * len(lst))]

def argmax(lst, fn):
    index, _ = max(enumerate(map(fn, lst)), key=lambda x: x[1])
    return index
