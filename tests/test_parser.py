# -*- coding: utf-8 -*-

from __future__ import absolute_import

import pytest

from type_doctor.parser import Parser


@pytest.fixture
def parser():
    return Parser()


def test_parse(parser):

    def a_test_func(x, y):
        # type: (int, int) -> int
        return x + y

    def another_test_func(x, y, z):
        # type: (int, str, int) -> int, str
        return 'hello worlr'

    assert parser.parse(a_test_func) == {'args': 'int, int', 'return': 'int'}
    assert parser.parse(another_test_func) == \
        {'args': 'int, str, int', 'return': 'int, str'}
