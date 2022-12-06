import signal
import sys
import traceback
from arsenal import colors
from arsenal.timer import htime, time

from argparse import ArgumentParser
from contextlib import contextmanager
from IPython.core import ultratb

from arsenal.maths import restore_random_state


class TestingFramework:

    def __init__(self, tests):

        p = ArgumentParser()
        p.add_argument('filters', nargs='*',
                       help='Include tests which contains any of these substrings.')
        p.add_argument('--skip', nargs='*',
                       help='Exclude tests which contains any of these substrings.',
                       default=[])

        # Random seed control
        p.add_argument('--seed', type=int, default=None)
        p.add_argument('--seed-scan', type=int, default=None)
        self.p = p

        self.overview = OverviewManager(True, False)
        self.tests = tests
        self.cli = p

    @property
    def args(self):
        return self.cli.parse_args()

    def run(self):
        # figure out which random seeds the user wants
        args = self.args
        if args.seed_scan is not None:
            # random seed search for trying to find a failing example.
            assert args.seed_scan > 0
            start_seed = args.seed or 0
            seeds = range(start_seed, start_seed + args.seed_scan)
        else:
            seeds = [args.seed]

        for name in self.find_tests():
            print(colors.light.yellow % colors.thick_line(80))
            print(colors.light.yellow % f'{name}')
            for seed in seeds:
                with restore_random_state(seed):
                    with self.overview(f'{name} (seed={seed})' if seed is not None else f'{name}'):
                        self.tests[name]()
            print()
        self.overview.report()

    def find_tests(self):
        args = self.args
        filters = list(args.filters) if args.filters else ['test_', 'todo_']
        for kw in filters:
            kw = kw.lower()
            for name in sorted(self.tests):
                x = name.lower()
                if (kw in x
                    and (x.startswith('test_') or x.startswith('todo_'))
                    and not any((z in x) for z in args.skip)
                ):
                    yield name


def testing_framework(tests):
    return TestingFramework(tests).run()


class FailedTest(Exception): pass


class OverviewManager:

    def __init__(self, overview, fancy_traceback=False):
        self.passed = 0
        self.failed = 0
        self.overview = overview
        self.fancy_traceback = fancy_traceback
        self.summary = []
        self.callback = None

        # Hardcoded log file
        #self.f = open('failed', 'w')   # track recent failure tests and run those first.

        # When the user send sigquit, we will still try to print the test
        # summary (i.e., call `report` with whatever progress was made).
        #
        # TODO: it'd be better if we also printed which tests did not get run,
        # but the current scheme, but the current usage does not make that easy.
        signal.signal(signal.SIGQUIT, self.SIGQUIT)

        self.suppress_exceptions = (KeyboardInterrupt,)

    def SIGQUIT(self, sig, frame):   # pylint: disable=unused-argument
        self.report()
        exit()

    @contextmanager
    def __call__(self, name):
        print()
        print(colors.yellow % colors.line(80))
        print(colors.yellow % 'Running %s' % name)

        b4 = time()
        if self.overview:
            try:
                yield
            except (KeyboardInterrupt, Exception) as e:          # pylint: disable=broad-except
                if self.callback is not None: self.callback(e)
                if self.fancy_traceback:
                    #exc = ultratb.FormattedTB(mode='Context')
                    exc = ultratb.FormattedTB(mode='Verbose')
                    exc(*sys.exc_info())
                else:
                    msg = ''.join(traceback.format_exception(*sys.exc_info()))
                    if isinstance(e, self.suppress_exceptions):
                        print(e.__class__.__name__, msg)
                    elif isinstance(e, (AssertionError, FailedTest)):
                        print(colors.render(colors.light.red % msg))
                    else:
                        print(colors.render(colors.red % msg))
                self.summary.append('%s %s: %s %s' % (colors.red % 'fail', name, type(e).__name__, colors.render(e)))
                self.failed += 1
                #print(name, file=self.f); self.f.flush()

            else:
                self.summary.append('%s %s' % (colors.green % 'pass', name))
                self.passed += 1
        else:
            yield

        took = time() - b4
        t = colors.magenta % f'({took:.3g}s)'
        print(colors.yellow % f'done {t}')

    def report(self):
        if not self.overview: return
        print()
        print(colors.light.yellow % 'Summary')
        print(colors.light.yellow % colors.thick_line(80))
        for x in sorted(self.summary, key=lambda x: 'fail' in x):
            print(x)
        print()
        print(f'passed: {self.passed}, failed: {self.failed}.')
