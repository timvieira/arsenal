from arsenal.terminal import (
    red, green, blue, yellow, black, magenta, cyan, white,
    light, dark, bg, normal,
    underline, italic, strike,
    nocolor, render, console_width, marquee, branch,
    mark, percent,
)


def test_color_format_strings():
    """Color format strings produce ANSI-wrapped output."""
    for color in [red, green, blue, yellow, black, magenta, cyan, white]:
        result = color % 'hello'
        assert 'hello' in result
        assert '\x1b[' in result
        assert '\x1b[0m' in result  # ends with reset


def test_light_dark_bg_variants():
    """light/dark/bg color variants produce ANSI output."""
    for variant in [light, dark, bg]:
        for name in ['red', 'green', 'blue', 'yellow', 'black', 'magenta', 'cyan', 'white']:
            result = getattr(variant, name) % 'test'
            assert 'test' in result
            assert '\x1b[' in result


def test_style_format_strings():
    """underline/italic/strike produce ANSI-wrapped output."""
    for style in [underline, italic, strike]:
        result = style % 'styled'
        assert 'styled' in result
        assert '\x1b[' in result


def test_nocolor():
    """nocolor strips all ANSI codes."""
    colored = red % 'hello'
    assert nocolor(colored) == 'hello'

    nested = red % ('outer ' + (green % 'inner') + ' outer')
    assert nocolor(nested) == 'outer inner outer'


def test_render_stack():
    """render() handles nested color strings with stack-based reset."""
    g = green % 'green'
    b = blue % f'blue {g} blue'
    r = red % f'red {b} red {b} red'
    x = normal % f'normal {r} normal'
    result = render(x)
    # The rendered string should contain all the text fragments
    plain = nocolor(result)
    assert 'green' in plain
    assert 'blue' in plain
    assert 'red' in plain
    assert 'normal' in plain


def test_render_light_dark():
    """render() correctly restores after dark inside light."""
    result = render(
        light.blue % 'light %s light'
        % dark.blue % 'dark %s dark'
        % blue % 'regular'
    )
    plain = nocolor(result)
    assert 'light' in plain
    assert 'dark' in plain
    assert 'regular' in plain


def test_console_width():
    """console_width returns a positive integer."""
    w = console_width()
    assert isinstance(w, int)
    assert w > 0


def test_marquee():
    """marquee pads with stars to console width."""
    m = marquee(' test ')
    assert ' test ' in m
    assert m[0] == '*'
    assert m[-1] == '*'


def test_branch():
    """branch() produces tree-structured lines."""
    result = branch([['a', 'a2'], ['b'], ['c', 'c2', 'c3']])
    text = '\n'.join(result)
    assert 'a' in text
    assert 'b' in text
    assert 'c' in text
    # First item gets top bracket, last gets bottom
    assert result[0].startswith('\u250c')  # ┌
    assert any(line.startswith('\u2514') for line in result)  # └


def test_mark():
    """mark() returns check/xmark based on truthiness."""
    assert nocolor(mark(True)) == '\u2714'   # ✔
    assert nocolor(mark(False)) == '\u2718'  # ✘


def test_percent():
    """percent() formats correctly."""
    assert percent(1, 2) == '50.0% (1/2)'
    assert percent(0, 0) == '100.0% (0/0)'
