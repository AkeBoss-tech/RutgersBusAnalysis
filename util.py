
def printAny(object):
    for attr in dir(object):
        if not attr.startswith('_'):
            print(attr, getattr(object, attr))

    