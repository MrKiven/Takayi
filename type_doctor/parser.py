# -*- coding: utf-8 -*-

import inspect
import re

from type_doctor.exc import ParseTypeError

"""
    def ham(x, y):
        # type: (int, str) -> str
        # docstring here

    parse first line of docstring:
        type: (int, str) -> str

"""

parse_type_hints = re.compile(r'''
(?P<start>[# type:]+)\(
(?P<args>[\w+, ]+)\).*->.*?
(?P<return>[\w+, ]+)
''', re.X)


class Parser(object):

    def __init__(self):
        self._start = 'start'
        self.parse_pattern = re.compile(r'''
            (?P<{}>[# type:]+)\(
            (?P<args>[\w+, ]+)\).?->.?
            (?P<return>[\w+, ]*)
            '''.format(self._start), re.X)

    def parse(self, func):
        """Parse first line of 'docstring'"""
        type_docs = inspect.getsourcelines(func)[0][1].strip()
        return self._match_types(type_docs)

    def _match_types(self, type_docs):
        """Match given string.

        :return: a dict, e.g.
            {'start': '# type: ', 'args': 'int, int', 'return': 'int'}
        """
        match = self.parse_pattern.match(type_docs)
        result = None
        try:
            result = match.groupdict()
            if self._start in result:
                result.pop(self._start)
            return result
        except KeyError:
            return result
        except BaseException:
            raise ParseTypeError("Invalid type hints: {!r} ".format(type_docs))
