"""manual: Marker for marking tests as manual tests."""
import pytest


def pytest_configure(config):
    config.addinivalue_line("markers", __doc__.splitlines()[0])


def pytest_addoption(parser):
    """Adds options for the `manual` marker."""
    parser.addoption(
        "--manual",
        action="store_true",
        default=False,
        help="Collect manual tests (only for --collect-only)",
    )
    parser.addoption(
        "--include-manual",
        action="store_true",
        default=False,
        help="Collect also manual tests (only for --collect-only)",
    )


@pytest.mark.tryfirst
def pytest_collection_modifyitems(config, items):
    # prevent on slave nodes (xdist)
    if hasattr(config, "slaveinput"):
        return

    if config.getvalue("include_manual"):
        return

    is_manual = config.getvalue("manual")

    keep, discard = [], []
    for item in items:
        if bool(item.get_marker("manual")) == is_manual:
            keep.append(item)
        else:
            discard.append(item)

    items[:] = keep
    config.hook.pytest_deselected(items=discard)
