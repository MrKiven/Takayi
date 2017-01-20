# -*- coding: utf-8 -*-

"""
  https://hg.python.org/cpython/file/3.6/Lib/typing.py
"""


class AnyObject(object):
    pass


_transition = {
    'Int': int,
    'List': list,
    'Dict': dict,
    'String': (str, basestring),
    'Mapping': dict,
    'Any': AnyObject,
    'Set': set,
    'Callable': callable,
    'Tuple': tuple,
    'Iterable': iter,
    'Sequence': (list, dict, set)
}


class TypingMeta(type):

    def __new__(cls, name, bases, attrs):
        attrs['_typing'] = 'Typing'
        return super(TypingMeta, cls).__new__(cls, name, bases, attrs)


class TypeVar(object):
    __metaclass__ = TypingMeta

    def __init__(self, t_name):
        self.t_name = t_name


class _BaseType(object):
    __metaclass__ = TypingMeta

    def __init__(self, t_name):
        self.t_name = t_name
        if self.t_name not in _transition:
            raise TypeError("No such type: %s" % self.t_name)
        self.t_type = _transition[self.t_name]
        self.t_item = None

    def __getitem__(self, name):
        self.t_item = name
        return self

    def __str__(self):
        s = "%s.%s" % (self._typing, self.t_name)
        if self.t_item:
            s += '[%s]' % self.t_item
        return s

    def __repr__(self):
        return '<{}>'.format(str(self))


def is_type(obj, ins):
    assert isinstance(ins, _BaseType), "Invalid type: {}".format(ins)
    t_type = ins.t_type
    t_name = ins.t_name
    if t_name == 'Callable':
        return callable(obj)
    if t_name == 'Any':
        return True
    return isinstance(obj, t_type)


Int = _BaseType('Int')
Any = _BaseType('Any')
String = _BaseType('String')
List = _BaseType('List')
Mapping = _BaseType('Mapping')
Set = _BaseType('Set')
Callable = _BaseType('Callable')
Tuple = _BaseType('Tuple')
Iter = _BaseType('Iterable')
Sequence = _BaseType('Sequence')
