from gepy.decorators import symbol
from gepy.genes import ReturnValue

@symbol("add")
def add(stack):
    stack.append(stack.pop() + stack.pop())
    return stack

@symbol("mul")
def mul(stack):
    stack.append(stack.pop() * stack.pop())
    return stack

@symbol("sub")
def sub(stack):
    stack.append(stack.pop() - stack.pop())
    return stack

@symbol("div")
def div(stack):
    stack.append(stack.pop() / stack.pop())
    return stack

@symbol("inc")
def inc(stack):
    stack.append(stack.pop() + 1.0)
    return stack

@symbol("dec")
def dec(stack):
    stack.append(stack.pop() - 1.0)
    return stack

@symbol("dup")
def dup(stack):
    a = stack[-1]
    stack.append(a)
    return stack

@symbol("swap")
def swap(stack):
    a = stack.pop()
    b = stack.pop()
    stack.append(a)
    stack.append(b)
    return stack

@symbol("nop")
def nop(stack):
    return stack

@symbol("ret")
def ret(stack):
    raise ReturnValue(stack[-1])
