from arsenal.misc import redirect_io


def test_redirect_io():
    msg = 'hello there?'
    with redirect_io() as f:
        print(msg)
    assert str(f.getvalue().strip()) == msg
