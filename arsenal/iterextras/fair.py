from itertools import cycle, islice


def _fair_product(A, B):
    """
    Cartesian product of two possibly infinite iterables
    Based closely on https://github.com/sympy/sympy/issues/17157
    """

    A = iter(A)
    B = iter(B)

    a = []
    b = []

    sentinel = object()
    def append(it, elems):
        e = next(it, sentinel)
        if e is not sentinel:
            elems.append(e)

    n = 0
    append(A, a)
    append(B, b)

    while n <= len(a) + len(b):
        for m in range(n-len(a)+1, len(b)):
            yield (a[n-m], b[m])
        n += 1
        append(A, a)
        append(B, b)


def fair_product(*iterables):
    """
    Returns Cartesian product of iterables. Yields every element
    eventually.

    Based closely on https://github.com/sympy/sympy/issues/17157
    """
    if len(iterables) == 0:
        yield ()
        return
    elif len(iterables) == 1:
        for e in iterables[0]:
            yield (e,)
    elif len(iterables) == 2:
        for e12 in _fair_product(*iterables):
            yield e12
    else:
        first, *others = iterables
        for ef, eo in fair_product(first, fair_product(*others)):
            yield (ef,) + eo



def merge_roundrobin(*iterables):
    """
    Merge iterators with a round-robin scheduler.
    Original implementation by George Sakkis.

    >>> list(merge_roundrobin('ABC', 'D', 'EF'))
    ['A', 'D', 'E', 'B', 'F', 'C']

    >>> from itertools import count
    >>> from arsenal.iterextras.util import take
    >>> list(take(10, merge_roundrobin('ABC', count(), 'E')))
    ['A', 0, 'E', 'B', 1, 'C', 2, 3, 4, 5]

    """
    pending = len(iterables)
    nexts = cycle(iter(it).__next__ for it in iterables)
    while pending:
        try:
            for _next in nexts:
                yield _next()
        except StopIteration:
            pending -= 1
            nexts = cycle(islice(nexts, pending))

fair_union = merge_roundrobin


def test_fair_product():
    from itertools import count

    def show_cross_product(xys, steps, N):
        grid = [['  .' for j in range(N)] for i in range(N)]
        for i, (x, y) in enumerate(xys):
            if i >= steps: break
            try:
                grid[x][y] = f'{i:3d}'
            except IndexError:
                pass
        print('[%s]' % ( ']\n['.join(' '.join(map(str,row)) for row in grid)))


    N = 10
    steps = N*(N+1)//2

    from arsenal import colors
    print()
    print(colors.light.yellow % 'fair_product: inf-inf')
    show_cross_product(fair_product(count(), count()),
                       steps = steps, N = N)

    print()
    print(colors.light.yellow % 'fair_product: inf-fin')
    show_cross_product(fair_product(count(), range(4)),
                       steps = steps, N = N)

    print()
    print(colors.light.yellow % 'fair_product: fin-inf')
    show_cross_product(fair_product(range(4), count()),
                       steps = steps, N = N)

    print()
    print(colors.light.yellow % 'fair_product: fin-fin')
    show_cross_product(fair_product(range(3), range(5)),
                       steps = steps, N = N)


if __name__ == '__main__':
    test_fair_product()

    import doctest
    doctest.testmod()
