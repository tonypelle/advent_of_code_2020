import functools

def mult(args):
    return functools.reduce(lambda x, y: x*y, args)
