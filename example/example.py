# -*- coding: utf-8 -*-

from takayi.parser import Parser, typehints


parser = Parser()


class Node(object):

    def __init__(self, x, y):
        self.x = x
        self.y = y

node = Node(1, 2)


@typehints(parser, attach_cls=Node)
def get_node():
    # type: () -> Node
    return node


@typehints(parser, attach_cls=Node)
def get_node_error():
    # type: () -> Node
    return 'hello'


@typehints(parser)
def get_int(i):
    # type: (int) -> int
    return i


@typehints(parser)
def get_str(s):
    # type: (str) -> str
    return s


@typehints(parser)
def get_tuple(x, y):
    # type: (int, str) -> tuple
    return x, y


@typehints(parser)
def send_args(x, y):
    # type: (int, str) -> str
    return 'hello'


@typehints(parser)
def no_args():
    # type: () -> int
    return 1
