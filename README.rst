====================
pytest-manual-marker
====================

Pytest marker for marking manual tests. Adds options for collecting manual, automated (default) or both.


Usage
-----
Collect tests data::

    $ py.test --collect-only --manual  # collect only manual tests
    $ py.test --collect-only --include-manual  # collect both manual and automated tests

Install
-------
Install this plugin::

    $ pip install pytest-manual-marker
