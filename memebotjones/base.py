# This is mostly ripped off from cacobot.
# It allows easier declaration of commands
# Add the @base.memefunc decorator to any function, and the name of the function becomes a command
functions = {}


def memefunc(func):
    functions[func.__name__] = func
    return func
