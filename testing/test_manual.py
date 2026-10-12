def test_collection(pytester):
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
    res = pytester.runpytest("-m", "not manual")
    res.assert_outcomes(passed=1, failed=0, errors=0, skipped=0)

    res_included = pytester.runpytest()
    parsed = dict(res_included.parseoutcomes())
    assert "manual" in parsed
    print(parsed)
    res_included.assert_outcomes(passed=1, failed=0, errors=0, skipped=0, xfailed=0)


def test_manual_only_deselects_automated(pytester):
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
    res = pytester.runpytest("--manual-only", "-v")
    res.stdout.fnmatch_lines(["*::test_manual MANUAL*", "*1 deselected*"])
    res.stdout.no_fnmatch_line("*test_automated*")
    assert res.ret == 0
