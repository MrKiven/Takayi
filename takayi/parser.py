# -*- coding: utf-8 -*-

import inspect
import re
import functools

from .exc import ParseTypeError, InvalidHintsError, \
    ParameterTypeError, ReturnTypeError

"""
    def ham(x, y):
        # type: (int, str) -> str
        # docstring here

    parse first line of docstring:
        type: (int, str) -> str

"""

START = 'start'

parse_pattern = re.compile(r'''
    (?P<{}>[# type:]+)\(
    (?P<args>[(\w+: )*\w+, ]*)\).?->.?
    (?P<return>[\w+, ]*)
    '''.format(START), re.X)


_transmit_mapping = {
    'int': int,
    'str': str,
    'dict': dict,
    'list': list,
    'tuple': tuple,
    'set': set,
    'any': (int, str, dict, list, tuple, set)
}


class TypeHints(object):

    def __init__(self, func_name, arg_types, return_types):
        self.func_name = func_name
        self.arg_types = arg_types
        self.return_types = return_types
        self.transmit_mapping = _transmit_mapping

    def attach_type(self, name, t_type):
        if name not in self.transmit_mapping:
            self.transmit_mapping[name] = t_type

    def _get_type(self, t_type):
        if ':' in t_type:
            t_type = t_type.split(':')[-1].strip()
        try:
            return self.transmit_mapping[t_type]
        except KeyError:
            raise TypeError("No such type: {!r}, you should attach this type "
                            "to parser first".format(t_type))

    @property
    def args(self):
        return map(lambda t: self._get_type(t), self.arg_types)

    @property
    def returns(self):
        return map(lambda t: self._get_type(t), self.return_types)

    @property
    def typehints(self):
        return self

    def __str__(self):
        """
        e.g. test(int, int) -> int
        """
        args = ''
        returns = ''
        for arg in self.arg_types:
            args += ''.join((arg, ', '))
        for ret in self.return_types:
            returns += ''.join((ret, ', '))
        # also remove the space
        return self.func_name + '(' + args[:-2] + ')' + ' -> ' + returns[:-2]

    def __repr__(self):
        return str(self)


def typehints(parser, attach_cls=None):
    """Decorator for typehints current function.

    Example:
        parser = Parser()

        class Node(object): pass
        node = Node()

        @typehints(attach_cls=Node)
        def get_node(what):
            # type: (str) -> Node
            return node

    parser: instance of :claass:`Parser`
    attach_cls: custom class
    """
    def mid_func(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # mark param `deco` to `True`
            hints = parser.parse(func, deco=True)
            if attach_cls:
                hints.attach_type(attach_cls.__name__, attach_cls)
            actually_args = map(lambda x: type(x), args)
            if kwargs:
                actually_args += map(lambda x: type(x), kwargs.itervalues())
            if actually_args:
                if not actually_args == hints.args:
                    raise ParameterTypeError(
                        "Expect => {}, Actually => {}".format(
                            hints.args, actually_args))

            ret = func(*args, **kwargs)
            actually_returns = map(lambda x: type(x), [ret])
            if not actually_returns == hints.returns:
                raise ReturnTypeError(
                    "Expect => {}, Actually => {}".format(
                        hints.returns, actually_returns))

            return ret
        return wrapper
    return mid_func


class Parser(object):

    def __init__(self, pattern=parse_pattern):
        self._start = START
        self.pattern = pattern
        self.attached_types = {}

    def parse(self, func, deco=False):
        """Parse first line of 'docstring'

        :param func: function to parse
        :param deco: Only use when using `typehints` decorator
        :return: :class:`TypeHints`
        """
        line = 2 if deco else 1
        type_docs = inspect.getsourcelines(func)[0][line].strip()
        if not type_docs.startswith('# type:'):
            raise InvalidHintsError("First line must be start like: `# type:`")
        drafts = self._match_types(type_docs)
        return self._parse(func.__name__, drafts)

    def _parse(self, name, t_d):
        if 'args' not in t_d and 'return' not in t_d:
            raise ParseTypeError("Parse err: %s" % t_d)
        args_types = [t.strip() for t in t_d['args'].split(',')]
        return_types = [t.strip() for t in t_d['return'].split(',')]
        return TypeHints(name, args_types, return_types)

    def _match_types(self, type_docs):
        """Match given string.

        :return: a dict, e.g.
            {'args': 'int, int', 'return': 'int'}
        """
        match = self.pattern.match(type_docs)
        result = None
        try:
            result = match.groupdict()
            if self._start in result:
                # useless key: `start`, pop it
                result.pop(self._start)
            return result
        except KeyError:
            return result
        except BaseException:
            raise ParseTypeError("Invalid type hints: {!r} ".format(type_docs))
