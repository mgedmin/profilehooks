"""
Tests for profilehooks.py

Run it with python setup.py test
"""

import sys
import doctest
import unittest
import StringIO

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

    Ever call also prints to stderr

        >>> print sys.stderr.getvalue()
        <BLANKLINE>
          sample_fn (<doctest test_profilehooks.doctest_timecall[0]>:1):
            0.000 seconds
        <BLANKLINE>
        <BLANKLINE>

    """


def setUp(test):
    test.real_stderr = sys.stderr
    stderr_wrapper = StringIO.StringIO()
    sys.stderr = stderr_wrapper


def tearDown(test):
    sys.stderr = test.real_stderr


def additional_tests():
    return doctest.DocTestSuite(setUp=setUp, tearDown=tearDown)


if __name__ == '__main__':
    unittest.main(testSuite='additional_tests')

