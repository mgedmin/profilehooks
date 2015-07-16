#!/usr/bin/env python
"""
Tests for profilehooks.py

They are woefully incomplete.

Run it with python setup.py test
"""

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


def skipIf(condition, reason):
    def decorator(fn):
        if condition:
            fn.__doc__ = 'Test skipped: %s' % reason
        return fn
    return decorator


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


def doctest_coverage_when_source_is_not_available(self):
    """Test for coverage.

        >>> @profilehooks.coverage
        ... def sample_fn(x, y, z):
        ...     if x == y == z:
        ...         print("%s" % (x, ))
        ...     elif x == y:
        ...         print("%s %s" % (x, z))
        ...     else:
        ...         print("%s %s %s" % (x, y, z))

        >>> sample_fn(1, 1, 1)
        1
        >>> sample_fn(1, 2, 3)
        1 2 3


        >>> run_exitfuncs()
        <BLANKLINE>
        *** COVERAGE RESULTS ***
        sample_fn (<doctest test_profilehooks.doctest_coverage_when_source_is_not_available[0]>:1)
        function called 2 times
        <BLANKLINE>
        cannot show coverage data since co_filename is None

    """


def doctest_FuncSource_no_source_lines():
    """Test for FuncSource

        >>> fs = profilehooks.FuncSource(doctest_FuncSource_no_source_lines)
        >>> fs.find_source_lines()
        >>> fs.firstcodelineno != 0
        True

    """


def doctest_FuncSource_no_source_file():
    """Test for FuncSource

    Define a function with a strange-looking filename

        >>> def mock_getsourcelines(fn):
        ...     raise IOError()

        >>> real_getsourcelines = inspect.getsourcelines
        >>> inspect.getsourcelines = mock_getsourcelines

        >>> fs = profilehooks.FuncSource(doctest_FuncSource_no_source_file)
        >>> fs.filename

        >>> inspect.getsourcelines = real_getsourcelines

    """


def doctest_profile():
    """Test for profile.

        >>> @profilehooks.profile
        ... def sample_fn(x, y, z):
        ...     print("%s %s %s" % (x, y, z))
        ...     return x + y * z

    You can call that function normally

        >>> r = sample_fn(1, 2, z=3)
        1 2 3
        >>> r
        7

    and do that more than once

        >>> sample_fn(3, 2, 1)
        3 2 1
        5

    When you exit, the profile is printed to stdout

        >>> run_exitfuncs()
        <BLANKLINE>
        *** PROFILER RESULTS ***
        sample_fn (<doctest test_profilehooks.doctest_profile[0]>:1)
        function called 2 times
        ...

    """


def doctest_profile_with_args():
    """Test for profile.

        >>> @profilehooks.profile(profiler='profile', skip=1,
        ...                       immediate=True, sort='calls')
        ... def sample_fn(x, y, z):
        ...     return x + y * z

    You can call that function a few times

        >>> sample_fn(1, 2, z=3)
        7
        >>> sample_fn(3, 2, 1)
        <BLANKLINE>
        *** PROFILER RESULTS ***
        sample_fn (<doctest test_profilehooks.doctest_profile_with_args[0]>:1)
        function called 2 times (1 calls not profiled)
        ...
        5

    """


def doctest_profile_with_bad_args():
    """Test for profile.

        >>> @profilehooks.profile(profiler='nosuch')
        ... def sample_fn(x, y, z):
        ...     return x + y * z
        Traceback (most recent call last):
          ...
        ValueError: only these profilers are available: ...profile...

    """


def doctest_profile_recursive_function():
    """Test for profile.

        >>> @profilehooks.profile(immediate=True)
        ... def fac(n):
        ...     if n < 1: return 1
        ...     return n * fac(n-1)

        >>> fac(3)
        <BLANKLINE>
        *** PROFILER RESULTS ***
        fac (<doctest test_profilehooks.doctest_profile_recursive_function[0]>:1)
        function called 4 times
        ...
        6

    """


@skipIf(profilehooks.hotshot is None, 'hotshot is not available')
def doctest_profile_with_hotshot():
    """Test for profile

        >>> @profilehooks.profile(immediate=True, profiler='hotshot', skip=2)
        ... def fac(n):
        ...     if n < 1: return 1
        ...     return n * fac(n-1)

        >>> fac(1)
        1

        >>> fac(3)
        <BLANKLINE>
        *** PROFILER RESULTS ***
        fac (<doctest test_profilehooks.doctest_profile_with_hotshot[0]>:1)
        function called 6 times (2 calls not profiled)
        ...
        6

    Hotshot leaves temporary files behind

        >>> os.unlink('fac.%d.prof' % os.getpid())

    """


@skipIf(profilehooks.hotshot is None, 'hotshot is not available')
def doctest_profile_with_hotshot_no_calls():
    """Test for profile

        >>> @profilehooks.profile(profiler='hotshot', filename='fac.prof')
        ... def fac(n):
        ...     if n < 1: return 1
        ...     return n * fac(n-1)

        >>> run_exitfuncs()
        <BLANKLINE>
        *** PROFILER RESULTS ***
        fac (<doctest test_profilehooks.doctest_profile_with_hotshot_no_calls[0]>:1)
        function called 0 times
        ...

        >>> os.unlink('fac.prof')

    """


def doctest_timecall():
    """Test for timecall.

        >>> @profilehooks.timecall
        ... def sample_fn(x, y, z):
        ...     print("%s %s %s" % (x, y, z))
        ...     return x + y * z

    You can call that function normally

        >>> r = sample_fn(1, 2, z=3)
        1 2 3
        >>> r
        7

    Every call also prints to stderr

        >>> print(sys.stderr.getvalue())
        <BLANKLINE>
          sample_fn (<doctest test_profilehooks.doctest_timecall[0]>:1):
            0.000 seconds
        <BLANKLINE>
        <BLANKLINE>

        >>> r = sample_fn(3, 2, 1)
        3 2 1

        >>> print(sys.stderr.getvalue())
        <BLANKLINE>
          sample_fn (<doctest test_profilehooks.doctest_timecall[0]>:1):
            0.000 seconds
        <BLANKLINE>
        <BLANKLINE>
          sample_fn (<doctest test_profilehooks.doctest_timecall[0]>:1):
            0.000 seconds
        <BLANKLINE>
        <BLANKLINE>

    """


def doctest_timecall_not_immediate():
    """Test for timecall.

        >>> @profilehooks.timecall(immediate=False)
        ... def sample_fn(x, y, z):
        ...     print('%s %s %s' % (x, y, z))
        ...     return x + y * z

    You can call that function normally

        >>> r = sample_fn(1, 2, z=3)
        1 2 3
        >>> r
        7

    This time nothing is printed to stderr

        >>> print(sys.stderr.getvalue())
        <BLANKLINE>

        >>> r = sample_fn(3, 2, 1)
        3 2 1

        >>> print(sys.stderr.getvalue())
        <BLANKLINE>

    until the application exits:

        >>> run_exitfuncs()
        <BLANKLINE>
          sample_fn (<doctest test_profilehooks.doctest_timecall_not_immediate[0]>:1):
            2 calls, 0.000 seconds (0.000 seconds per call)
        <BLANKLINE>

    """


def doctest_timecall_never_called():
    """Test for timecall.

        >>> @profilehooks.timecall(immediate=False)
        ... def sample_fn(x, y, z):
        ...     print("%s %s %s" % (x, y, z))
        ...     return x + y * z

        >>> run_exitfuncs()

    """


def doctest_dump():
    """Test that profiling can save the stats in a file.

    Create a temporary file

        >>> import tempfile
        >>> tf = tempfile.mkstemp()

    Now create some stats in that file

        >>> @profilehooks.profile(filename=tf[1])
        ... def f():
        ...     pass
        >>> run_exitfuncs() # doctest:+ELLIPSIS
        <BLANKLINE>
        ...
        <BLANKLINE>

    Let's see whether we can open the stats

        >>> import pstats
        >>> pstats.Stats(tf[1]) # doctest:+ELLIPSIS
        <pstats.Stats...>

    Remove the temporary file again

        >>> import os
        >>> os.close(tf[0])
        >>> os.remove(tf[1])

    """


def setUp(test):
    test.real_stderr = sys.stderr
    test.real_register = atexit.register
    stderr_wrapper = StringIO()
    sys.stderr = stderr_wrapper
    atexit.register = _register_exitfunc
    del _exitfuncs[:]
    test.real_time = time.time
    time.time = lambda: 1411735756


def tearDown(test):
    sys.stderr = test.real_stderr
    atexit.register = test.real_register
    del _exitfuncs[:]
    time.time = test.real_time


def additional_tests():
    optionflags = (doctest.REPORT_ONLY_FIRST_FAILURE |
                   doctest.ELLIPSIS)
    return unittest.TestSuite([
        unittest.defaultTestLoader.loadTestsFromName(__name__),
        doctest.DocTestSuite(setUp=setUp, tearDown=tearDown,
                                optionflags=optionflags),
    ])


if __name__ == '__main__':
    # a bit pointless: __name__ is different and thus all tests will fail
    __name__ = 'test_profilehooks'
    sys.modules[__name__] = sys.modules['__main__']
    unittest.main(defaultTest='additional_tests')

