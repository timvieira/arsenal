import matplotlib
matplotlib.use('Agg')

from arsenal.viz.util import NumericalDebug, name2color, DEBUG


def test_numerical_debug_update():
    """NumericalDebug accumulates rows into a DataFrame."""
    d = NumericalDebug('test_nd')
    d.update(want=1, have=1)
    d.update(want=1, have=1.01)
    d.update(want=1, have=0.99)

    df = d.df
    assert len(df) == 3
    assert list(df.columns) == ['want', 'have']
    assert df['want'].tolist() == [1, 1, 1]
    assert df['have'].tolist() == [1, 1.01, 0.99]


def test_numerical_debug_empty():
    """Empty NumericalDebug has empty df."""
    d = NumericalDebug('test_empty')
    assert d.df is None or len(d._data) == 0


def test_debug_global_dict():
    """DEBUG global dict creates NumericalDebug instances on access."""
    d = DEBUG['test_global']
    assert isinstance(d, NumericalDebug)
    assert d.name == 'test_global'


def test_name2color():
    """name2color returns distinct colors for distinct names."""
    nc = name2color()
    c1 = nc['a']
    c2 = nc['b']
    c3 = nc['c']
    assert c1 != c2
    assert c2 != c3
    # Same name returns same color
    assert nc['a'] == c1
