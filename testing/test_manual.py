import attr
import pytest

try:
    from _pytest.pytester import Pytester
except ImportError:
    from _pytest.pytester import Testdir

    @attr.s(auto_attribs=True)
    class Pytester:  # type: ignore
        testdir: Testdir

        def __getattr__(self, name):
            return getattr(self.testdir, name)

    @pytest.fixture
    def pytester(testdir: Testdir) -> Pytester:
        return Pytester(testdir)  # type: ignore


def test_collection(pytester: Pytester):
    pytester.makepyfile(
        """
    import pytest

    @pytest.mark.manual
    def test_manual():
        pass

    def test_automated():
        pass
    """
    )
    res = pytester.runpytest()
    res.assert_outcomes(passed=1, failed=0, errors=0, skipped=0)

    res_included = pytester.runpytest("--include-manual")
    parsed = dict(res_included.parseoutcomes())
    assert "manual" in parsed
    print(parsed)
    res_included.assert_outcomes(passed=1, failed=0, errors=0, skipped=0, xfailed=0)
