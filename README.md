
# pytest-manual-marker

Pytest marker for tests that need a person to execute them.

Tests marked `manual` are not run; they are reported with their own
`manual` outcome (`M` in the progress line) instead of passing or failing.

## Usage

```python
# content of test_manual.py
import pytest


@pytest.mark.manual
def test_manual():
    """this needs a person to run it and reports MANUAL as its outcome"""


def test_automated():
    """an empty automated test, for show"""
```

### run everything, reporting manual tests

```console
$ pytest -q
M.                                                                       [100%]
1 passed, 1 manual in 0.01s
```

### only manual tests

```console
$ pytest -q --manual-only
M                                                                        [100%]
1 deselected, 1 manual in 0.01s
```

### only automated tests

```console
$ pytest -q -m "not manual"
.                                                                        [100%]
1 passed, 1 deselected in 0.00s
```

## Install

```console
$ pip install pytest-manual-marker
```
