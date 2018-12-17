from gepy.decorators import symbol

@symbol("EQ")
def cmp_eq(i, j):
    return float(i == j)

@symbol("NEQ")
def cmp_neq(i, j):
    return float(i != j)

@symbol("GT")
def cmp_gt(i, j):
    return float(i > j)

@symbol("GTE")
def cmp_gte(i, j):
    return float(i >= j)

@symbol("LT")
def cmp_lt(i, j):
    return float(i < j)

@symbol("LTE")
def cmp_lte(i, j):
    return float(i <= j)
