# -*- coding: utf-8 -*-

from __future__ import absolute_import

import pytest

from takayi.parser import Parser, typehints
from takayi.exc import ParseTypeError, InvalidHintsError, \
    ParameterTypeError, ReturnTypeError


@pytest.fixture
def parser():
    return Parser()


def test_parse(parser):

    def func(x):
        # type: (int) -> int
        return x

    hints = parser.parse(func)
    assert str(hints) == "func(int) -> int"
    assert hints.arg_types == ['int']
    assert hints.args == [int]
    assert hints.returns == [int]

    def a_test_func(x, y):
        # type: (int, int) -> int
        return x + y

    def another_test_func(x, y, z):
        # type: (int, str, int) -> int, str
        return 'hello world'

    h_a = parser.parse(a_test_func)
    assert str(h_a) == \
        "a_test_func(int, int) -> int"
    assert h_a.args == [int, int]
    assert h_a.returns == [int]

    h_b = parser.parse(another_test_func)
    assert str(h_b) == \
        "another_test_func(int, str, int) -> int, str"
    assert h_b.args == [int, str, int]
    assert h_b.returns == [int, str]

    def error_test_func(x):
        # type: str -> (str)
        return x

    with pytest.raises(ParseTypeError):
        parser.parse(error_test_func)

    def invalid_hints(x, y):
        # hahah
        return None

    with pytest.raises(InvalidHintsError):
        parser.parse(invalid_hints)


def test_custom_type(parser):

    class Test(object):
        pass

    t = Test()

    @typehints(parser, attach_cls=Test)
    def test(x, y):
        # type: (int, int) -> Test
        return t

    @typehints(parser, attach_cls=Test)
    def get_test():
        # type: () -> Test
        return t

    assert isinstance(test(1, 1), Test)
    assert isinstance(get_test(), Test)


def test_kwargs(parser):
    # not support yet..

    @typehints(parser)
    def func(x, y=1):
        # type: (int, y: int) -> int
        return x + y

    assert func(1, y=2) == 3
    with pytest.raises(ParameterTypeError):
        assert func(1, y='hello')
    with pytest.raises(ParameterTypeError):
        assert func('hello', y=10)


def test_decorator(parser):

    @typehints(parser)
    def no_args():
        # type: () -> int
        return 1

    @typehints(parser)
    def no_return():  # do nothing
        pass

    assert no_args() == 1

    @typehints(parser)
    def func(x, y):
        # type: (int, int) -> int
        return x + y

    assert func(1, 2) == 3
    with pytest.raises(ParameterTypeError):
        assert func('t', 1)

    @typehints(parser)
    def test(x, y):
        # type: (int, str) -> tuple
        return x, y
    assert test(1, 'test') == (1, 'test')
    with pytest.raises(ParameterTypeError):
        assert func('test', 1)

    @typehints(parser)
    def get_str(x, y):
        # type: (int, str) -> str
        return y

    assert get_str(1, 'hello') == 'hello'
    with pytest.raises(ParameterTypeError):
        assert get_str('hello', 1)

    @typehints(parser)
    def wrong_return():
        # type: () -> int
        return 'hello'
    with pytest.raises(ReturnTypeError):
        assert wrong_return()


def test_iterable_struct(parser):

    @typehints(parser)
    def get_books(num=2):
        # type: (num: int) -> list
        return [i for i in xrange(num)]

    assert get_books() == [0, 1]
    assert get_books(num=3) == [0, 1, 2]

    @typehints(parser)
    def get_phone(num=2):
        # type: (num: int) -> set
        return set([1, 2])
    assert get_phone() == set([1, 2])
