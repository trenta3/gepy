from gepy.decorators import symbol
import math

@symbol("floor")
def floor(i):
    return math.floor(i)

@symbol("ceil")
def ceil(i):
    return math.ceil(i)

@symbol("round")
def op_round(i):
    return round(i)
