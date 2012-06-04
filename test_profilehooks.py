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

try:
    from cStringIO import StringIO
except ImportError:
    from io import StringIO

import profilehooks


if hasattr(atexit, '_run_exitfuncs'):
    run_exitfuncs = atexit._run_exitfuncs
else:
    run_exitfuncs = sys.exitfunc


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
    return doctest.DocTestSuite(setUp=setUp, tearDown=tearDown,
                                optionflags=optionflags)


if __name__ == '__main__':
    # a bit pointless: __name__ is different and thus all tests will fail
    __name__ = 'test_profilehooks'
    sys.modules[__name__] = sys.modules['__main__']
    unittest.main(defaultTest='additional_tests')

