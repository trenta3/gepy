from gepy.decorators import symbol

@symbol("min")
def op_min(i, j):
    return min(i, j)

@symbol("max")
def op_max(i, j):
    return max(i, j)

