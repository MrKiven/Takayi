# Takayi
Type hints for python 2.X

## Usage

```
from takayi.parser import Parser, typehints

parser = Parser()


@typehints(parser)
def get_sum(x, y):
    # type: (int, int) -> int
    return x + y

_sum = get_sum(1, 2)  # -> 3
_err_sum = get_sum(1, 'hello')  # ->  AssertionError: Parameter err: except => [<type 'int'>, <type 'int'>], actually => [<type 'int'>, <type 'str'>]
```
