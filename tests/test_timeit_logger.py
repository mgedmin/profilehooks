import doctest
import logging
import profilehooks
import sys
import time
import unittest

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


def doctest_timecall_with_logger():
    """Test for timecall with logging
    >>> @profilehooks.timecall(immediate=True, log_name='logtest', log_level=logging.INFO)
    ... def example(a, delay=True):
    ...    if delay:
    ...        time.sleep(a)
    ...    return a
    >>> example(.1, delay=True)
    """


def additional_tests():
    optionflags = (doctest.REPORT_ONLY_FIRST_FAILURE |
                   doctest.ELLIPSIS)
    return unittest.TestSuite([
        unittest.defaultTestLoader.loadTestsFromName(__name__),
        doctest.DocTestSuite(optionflags=optionflags),
    ])



if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    __name__ = 'test_profilehooks'
    sys.modules[__name__] = sys.modules['__main__']
    unittest.main(defaultTest='additional_tests')
