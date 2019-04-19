from random import random
from math import floor
from inspect import getargspec

def arity(fn):
    """
    Function that returns the arity of a function.
    """
    if not hasattr(fn, "_arity"):
        fn._arity = len(getargspec(fn)[0])
    return fn._arity
    # return fn.func_code.co_argcount

def list_choose_rand_with_bias(list1, list2, num, bias=0):
    """
    Select 'num' random elements from the union of list1 and list2.
    The bias is: rand_el = bias * list1 + (1 - bias) * (list1 + list2)
    """
    result = []
    unionlist = list1 + list2
    for i in range(num):
        if random() >= bias:
            result.append(unionlist[floor(random() * len(unionlist))])
        else:
            result.append(list1[floor(random() * len(list1))])
    return result
    
def list_choose_rand(fromlist, num):
    """
    Select 'num' random elements from the list.
    """
    list_len = len(fromlist)
    return [fromlist[floor(random() * list_len)] for i in range(num)]

def choose_rand(lst):
    return lst[floor(random() * len(lst))]

def choose_rand_with_bias(list1, list2, bias=0):
    unionlist = list1 + list2
    return unionlist[floor(random() * len(unionlist))] if random() >= bias else list1[floor(random() * len(list1))]

def argmax(lst, fn):
    index, _ = max(enumerate(map(fn, lst)), key=lambda x: x[1])
    return index
