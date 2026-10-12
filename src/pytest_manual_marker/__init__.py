"""manual: mark tests which need a person to execute them"""

from collections.abc import Generator

import pytest

MANUAL = "manual"


def pytest_configure(config: pytest.Config) -> None:
    config.addinivalue_line("markers", __doc__.splitlines()[0])


def pytest_addoption(parser: pytest.Parser) -> None:
    group = parser.getgroup("manual", "configuration of manual tests")
    group.addoption(
        "--manual-only",
        action="store_true",
        default=False,
        help="deselect all automated tests, collects only manual tests",
    )


@pytest.hookimpl(tryfirst=True)
def pytest_runtest_setup(item: pytest.Item) -> None:
    mark = item.get_closest_marker(MANUAL)
    if mark is not None:
        # todo: filter valid
        pytest.xfail(MANUAL)


@pytest.hookimpl(wrapper=True, tryfirst=True)
def pytest_runtest_makereport(
    item: pytest.Item, call: pytest.CallInfo[None]
) -> Generator[None, pytest.TestReport, pytest.TestReport]:
    rep = yield
    if (
        call.excinfo
        and isinstance(call.excinfo.value, pytest.xfail.Exception)
        and call.excinfo.value.msg == MANUAL
    ):
        rep.outcome = MANUAL  # type: ignore[assignment]
    return rep


@pytest.hookimpl(tryfirst=True)
def pytest_report_teststatus(
    report: pytest.TestReport,
) -> tuple[str, str, str] | None:
    if report.outcome == MANUAL:
        return MANUAL, "M", MANUAL.upper()
    return None


@pytest.hookimpl(tryfirst=True)
def pytest_collection_modifyitems(
    config: pytest.Config, items: list[pytest.Item]
) -> None:
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
