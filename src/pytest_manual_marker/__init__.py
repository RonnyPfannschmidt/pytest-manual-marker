"""manual: mark tests which need a person to execute them"""

import pytest


def pytest_configure(config):
    config.addinivalue_line("markers", __doc__.splitlines()[0])


def pytest_addoption(parser):
    group = parser.getgroup("manual", "configuration of manual tests")
    group.addoption(
        "--manual",
        action="store_true",
        default=False,
        help="deselect all automated tests, collects only manual tests",
    )
    parser.addoption(
        "--include-manual",
        action="store_true",
        default=False,
        help="disables the default deslection of manual tests",
    )


@pytest.mark.tryfirst
def pytest_collection_modifyitems(config, items):
    # prevent on worker nodes (xdist)
    if hasattr(config, "workerinput"):
        return

    if config.getoption("include_manual"):
        return

    is_manual = config.getoption("manual")

    keep, discard = [], []
    for item in items:
        if (item.get_closest_marker("manual") is None) ^ is_manual:
            keep.append(item)
        else:
            discard.append(item)

    items[:] = keep
    config.hook.pytest_deselected(items=discard)
