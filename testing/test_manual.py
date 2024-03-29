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
