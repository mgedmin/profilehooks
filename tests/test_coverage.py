import os
import sys
import doctest
import unittest
import inspect
import atexit
import textwrap
import time

try:
    from cStringIO import StringIO
except ImportError:
    from io import StringIO

import profilehooks


_exitfuncs = []


def _register_exitfunc(func, *args, **kw):
    _exitfuncs.append((func, args, kw))


def run_exitfuncs():
    for fn, args, kw in _exitfuncs:
        fn(*args, **kw)


class TestCase(unittest.TestCase):

    maxDiff = None

    def setUp(self):
        self.real_stderr = sys.stderr
        self.real_stdout = sys.stdout
        self.real_register = atexit.register
        sys.stderr = StringIO()
        sys.stdout = StringIO()
        atexit.register = _register_exitfunc
        del _exitfuncs[:]

    def tearDown(self):
        sys.stderr = self.real_stderr
        sys.stdout = self.real_stdout
        atexit.register = self.real_register
        del _exitfuncs[:]


class TestCoverage(TestCase):

    # This is a unit test and not a doctest because inspect.getsource()
    # gets confused about functions defined in doctests.
    #
    # The downside of using a unit test is cumbersome checking of
    # stdout-printed text, and the inability of using the decorators
    # directly in the source, because we haven't stubbed atexit.register yet.

    def sample_fn(self, x, y, z):
        if x == y == z:
            return "%s" % (x, )
        elif x == y:
            return "%s %s" % (x, z)
        else:
            return "%s %s %s" % (x, y, z)

    def sample_fn_2(self):
        try:
            os.path.join('a', 'b')
        finally:
            x = 5
        del x

    decorator = staticmethod(profilehooks.coverage)

    if not hasattr(TestCase, 'assertMultiLineEqual'):  # Python 2.6
        assertMultiLineEqual = TestCase.assertEqual

    def test_coverage(self):
        sample_fn = self.decorator(self.sample_fn)
        sample_fn(1, 1, 1)
        sample_fn(1, 2, 3)
        linenumber = self.sample_fn.__code__.co_firstlineno
        run_exitfuncs()
        self.assertMultiLineEqual(
            sys.stdout.getvalue(),
            '\n' + textwrap.dedent("""\
            *** COVERAGE RESULTS ***
            sample_fn (test_profilehooks.py:{0})
            function called 2 times

                       def sample_fn(self, x, y, z):
                2:         if x == y == z:
                1:             return "%s" % (x, )
                1:         elif x == y:
            >>>>>>             return "%s %s" % (x, z)
                           else:
                1:             return "%s %s %s" % (x, y, z)

            1 lines were not executed.
            """.format(linenumber)))

    def test_coverage_again(self):
        sample_fn_2 = self.decorator(self.sample_fn_2)
        sample_fn_2()
        linenumber = self.sample_fn_2.__code__.co_firstlineno
        run_exitfuncs()
        self.assertMultiLineEqual(
            sys.stdout.getvalue(),
            '\n' + textwrap.dedent("""\
            *** COVERAGE RESULTS ***
            sample_fn_2 (test_profilehooks.py:{0})
            function called 1 times

                       def sample_fn_2(self):
                1:         try:
                1:             os.path.join('a', 'b')
                           finally:
                1:             x = 5
                1:         del x

            """.format(linenumber)))

if profilehooks.hotshot is not None:
    class TestCoverageWithHotShot(TestCoverage):
        decorator = staticmethod(profilehooks.coverage_with_hotshot)

        def tearDown(self):
            super(TestCoverageWithHotShot, self).tearDown()
            for name in 'sample_fn', 'sample_fn_2':
                try:
                    os.unlink('%s.%d.cprof' % (name, os.getpid()))
                except OSError:
                    pass

