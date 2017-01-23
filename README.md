# Takayi
Type hints for python 2.X

`takayi` means `high` in japanese..

## Usage

```python
from takayi.parser import Parser, typehints

parser = Parser()

# ==================================================
@typehints(parser)
def get_sum(x, y):
    # type: (int, int) -> int
    return x + y

_sum = get_sum(1, 2)  # -> 3

# takayi.exc.ParameterTypeError: Expect => [<type 'int'>, <type 'int'>], Actually => [<type 'int'>, <type 'str'>]
_err_sum = get_sum(1, 'hello')


# ==================================================
@typehints(parser)
def test(x, y=1)
    # type: (int, y: int) -> int
    return x + y

assert test(1, y=10) == 11


# ==================================================
class Node(object): pass

node = Node()


@typehints(parser, attach_cls=Node)
def get_node():
    # type: () -> Node
    return node
```

## TODO

- [x] Support kwargs type check
- [ ] More types. FYI: [pep484](https://www.python.org/dev/peps/pep-0484/)
