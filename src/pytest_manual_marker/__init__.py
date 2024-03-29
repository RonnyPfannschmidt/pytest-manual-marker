"""manual: mark tests which need a person to execute them"""
import pytest

MANUAL = "manual"


def pytest_configure(config):
    config.addinivalue_line("markers", __doc__.splitlines()[0])


def pytest_addoption(parser):
    group = parser.getgroup("manual", "configuration of manual tests")
    group.addoption(
        "--manual-only",
        action="store_true",
        default=False,
        help="deselect all automated tests, collects only manual tests",
    )


@pytest.hookimpl(tryfirst=True)
def pytest_runtest_setup(item: pytest.Item):
    mark = item.get_closest_marker(MANUAL)
    if mark is not None:
        # todo: filter valid
        pytest.xfail(MANUAL)


@pytest.hookimpl(hookwrapper=True, tryfirst=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    if call.excinfo and isinstance(call.excinfo.value, pytest.xfail.Exception):
        if call.excinfo.value.msg == MANUAL:
            rep.outcome = "manual"


@pytest.hookimpl(tryfirst=True)
def pytest_report_teststatus(report):
    if report.outcome == MANUAL:
        return MANUAL, "M", MANUAL.upper()


@pytest.hookimpl(tryfirst=True)
def pytest_collection_modifyitems(config, items):
    if not config.getoption("--manual-only"):
        return

    keep, discard = [], []
    for item in items:
        if item.get_closest_marker(MANUAL) is not None:
            keep.append(item)
        else:
            discard.append(item)

    items[:] = keep
    config.hook.pytest_deselected(items=discard)
