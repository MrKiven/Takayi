# -*- coding: utf-8 -*-

from __future__ import absolute_import

import pytest

from takayi.typing import Any, List, Mapping, Callable, Sequence, is_type,\
    String, AnyObject


def test_types():
    assert str(Any) == 'Typing.Any'
    assert str(List) == 'Typing.List'
    assert str(Mapping) == 'Typing.Mapping'
    assert str(Callable) == 'Typing.Callable'
    assert str(Sequence) == 'Typing.Sequence'
    assert str(String) == 'Typing.String'

    assert Any.t_name == 'Any'
    assert Any.t_type == AnyObject


def test_is_type():
    a_list = ['hello', 'world']
    a_mapping = {'hello': 'world'}
    a_str = 'hello world'

    with pytest.raises(AssertionError):
        is_type(a_str, str)

    def func():
        pass

    assert is_type(func, Callable) is True
    assert is_type(func, Any) is True
    assert is_type(func, List) is False

    assert is_type(a_list, List) is True
    assert is_type(a_list, Sequence) is True
    assert is_type(a_mapping, List) is False
    assert is_type(a_mapping, Sequence) is True

    assert is_type(a_list, Any) is True
    assert is_type(a_mapping, Any) is True

    assert is_type(a_list, Mapping) is False
    assert is_type(a_mapping, Mapping) is True

    assert is_type(a_str, String) is True
    assert is_type(a_str, Any) is True
    assert is_type(a_str, List) is False
