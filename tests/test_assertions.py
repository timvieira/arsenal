from arsenal.assertions import assert_throws


def test_assert_throws():
    with assert_throws(Exception):
        1/0

    with assert_throws(ZeroDivisionError):
        1/0

    with assert_throws(None):
        pass

    try:
        with assert_throws(ZeroDivisionError, TypeError, ValueError):
            pass
    except AssertionError:
        pass
    else:
        raise AssertionError('test failed.')
