"""
Tests for profilehooks.py

Run it with python setup.py test
"""

import sys
import doctest
import unittest
import StringIO
import atexit

import profilehooks


def doctest_timecall():
    """Test for timecall.

        >>> @profilehooks.timecall
        ... def sample_fn(x, y, z):
        ...     print x, y, z
        ...     return x + y * z

    You can call that function normally

        >>> r = sample_fn(1, 2, z=3)
        1 2 3
        >>> r
        7

    Every call also prints to stderr

        >>> print sys.stderr.getvalue(),
        <BLANKLINE>
          sample_fn (<doctest test_profilehooks.doctest_timecall[0]>:1):
            0.000 seconds
        <BLANKLINE>

        >>> r = sample_fn(3, 2, 1)
        3 2 1

        >>> print sys.stderr.getvalue(),
        <BLANKLINE>
          sample_fn (<doctest test_profilehooks.doctest_timecall[0]>:1):
            0.000 seconds
        <BLANKLINE>
        <BLANKLINE>
          sample_fn (<doctest test_profilehooks.doctest_timecall[0]>:1):
            0.000 seconds
        <BLANKLINE>

    """


def doctest_timecall_not_immediate():
    """Test for timecall.

        >>> @profilehooks.timecall(immediate=False)
        ... def sample_fn(x, y, z):
        ...     print x, y, z
        ...     return x + y * z

    You can call that function normally

        >>> r = sample_fn(1, 2, z=3)
        1 2 3
        >>> r
        7

    This time nothing is printed to stderr

        >>> print sys.stderr.getvalue(),

        >>> r = sample_fn(3, 2, 1)
        3 2 1

        >>> print sys.stderr.getvalue(),

    until the application exits:

        >>> sys.exitfunc()
        <BLANKLINE>
          sample_fn (<doctest test_profilehooks.doctest_timecall_not_immediate[0]>:1):
            2 calls, 0.000 seconds (0.000 seconds per call)
        <BLANKLINE>

    """


def setUp(test):
    test.real_stderr = sys.stderr
    stderr_wrapper = StringIO.StringIO()
    sys.stderr = stderr_wrapper


def tearDown(test):
    sys.stderr = test.real_stderr
    del atexit._exithandlers[:]


def additional_tests():
    return doctest.DocTestSuite(setUp=setUp, tearDown=tearDown)


if __name__ == '__main__':
    unittest.main(testSuite='additional_tests')

