from gepy.decorators import symbol
import math

@symbol("+")
def addition(i, j):
    return i + j

@symbol("-")
def subtraction(i, j):
    return i - j

@symbol("*")
def multiplication(i, j):
    return i * j

@symbol("/")
def division(i, j):
    return i / j

@symbol("^")
def power(i, j):
    return i ** j

@symbol("sqrt")
def sqrt(i):
    return math.sqrt(i)

@symbol("sin")
def sin(i):
    return math.sin(i)

@symbol("cos")
def cos(i):
    return math.cos(i)

@symbol("exp")
def exp(i):
    return math.exp(i)

@symbol("ln")
def ln(i):
    return math.ln(i)
