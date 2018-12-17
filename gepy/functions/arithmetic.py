from gepy.decorators import symbol

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
