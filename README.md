
# pytest-manual-marker

Pytest marker for marking manual tests. Adds options for collecting manual, automated (default) or both.

Adds a different test outcome for manaual tests.

## Usage

```python
# content of test_manual.py
import pytest

@pytest.mark.manual
def test_manual():
    """this needs a opt in and will report manual as test status"""

def test_automated():
    """this is a empty test just for shows"""
```


### collect only manual tests

```console
$ pytest --collect-only -q --manual
test_manual.py::test_manual

1/2 tests collected (1 deselected) in 0.00s
```

### collect only automated tests

```console
$ pytest --collect-only -q
test_manual.py::test_automated

1/2 tests collected (1 deselected) in 0.00s
```

### collect manual and automated tests

```console
$ pytest --collect-only -q --include-manual  # collect both manual and automated tests
test_manual.py::test_manual
test_manual.py::test_automated

2 tests collected in 0.00s
```

## Install

Install this plugin::

```console
! pip install pytest-manual-marker
```
