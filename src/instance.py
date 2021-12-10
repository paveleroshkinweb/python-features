def instance(obj, cls):
    if type(obj) is type:
        return cls is type
    mro = type(obj).mro()
    try:
        mro.index(cls)
        return True
    except IndexError:
        return False

