#!/usr/bin/env python
"""
Tests for profilehooks.py

They are woefully incomplete.

Run it with python setup.py test
"""

import sys
import doctest
import unittest
import atexit
import textwrap
import difflib

try:
    from cStringIO import StringIO
except ImportError:
    from io import StringIO

import profilehooks


if hasattr(atexit, '_run_exitfuncs'):
    run_exitfuncs = atexit._run_exitfuncs
else:
    run_exitfuncs = sys.exitfunc


class TestCase(unittest.TestCase):

    maxDiff = None

    def setUp(self):
        self.real_stderr = sys.stderr
        self.real_stdout = sys.stdout
        sys.stderr = StringIO()
        sys.stdout = StringIO()

    def tearDown(self):
        sys.stderr = self.real_stderr
        sys.stdout = self.real_stdout


class TestCoverage(TestCase):

    @profilehooks.coverage
    def sample_fn(self, x, y, z):
        if x == y == z:
            return "%s" % (x, )
        elif x == y:
            return "%s %s" % (x, z)
        else:
            return "%s %s %s" % (x, y, z)

    def test_coverage(self):
        self.sample_fn(1, 1, 1)
        self.sample_fn(1, 2, 3)
        run_exitfuncs()
        self.assertEqual(
            sys.stdout.getvalue(),
            '\n' + textwrap.dedent("""\
            *** COVERAGE RESULTS ***
            sample_fn (test_profilehooks.py:48)
            function called 2 times

                       @profilehooks.coverage
                       def sample_fn(self, x, y, z):
                2:         if x == y == z:
                1:             return "%s" % (x, )
                1:         elif x == y:
            >>>>>>             return "%s %s" % (x, z)
                           else:
                1:             return "%s %s %s" % (x, y, z)

            1 lines were not executed.
            """))


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
        >>> os.remove(tf[1])

    """


def setUp(test):
    test.real_stderr = sys.stderr
    stderr_wrapper = StringIO()
    sys.stderr = stderr_wrapper


def tearDown(test):
    sys.stderr = test.real_stderr
    if hasattr(atexit, '_clear'):
        atexit._clear()
    else:
        del atexit._exithandlers[:]


def additional_tests():
    optionflags = (doctest.REPORT_ONLY_FIRST_FAILURE |
                   doctest.ELLIPSIS)
    return unittest.TestSuite([
        unittest.makeSuite(TestCoverage),
        doctest.DocTestSuite(setUp=setUp, tearDown=tearDown,
                                optionflags=optionflags),
    ])


if __name__ == '__main__':
    # a bit pointless: __name__ is different and thus all tests will fail
    __name__ = 'test_profilehooks'
    sys.modules[__name__] = sys.modules['__main__']
    unittest.main(defaultTest='additional_tests')

