
def symbol(symb):
    def wrapper(fn):
        fn._symbol = symb
        return fn
    return wrapper
