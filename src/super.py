from functools import partial


class SuperProxy:

    def __init__(self, cls, obj):
        self.__cls = cls
        self.__obj = obj

    def __getattr__(self, item):
        attr = self.__cls.__dict__[item]
        if callable(attr):
            return partial(attr, self.__obj)
        return attr


def _super(cls, obj):
    mro_list = type(obj).mro()
    current_class_index = mro_list.index(cls)
    next_super = mro_list[current_class_index + 1]
    return SuperProxy(next_super, obj)
