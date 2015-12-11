profilehooks
============

.. image:: https://travis-ci.org/mgedmin/profilehooks.svg?branch=master
   :target: https://travis-ci.org/mgedmin/profilehooks

.. image:: https://ci.appveyor.com/api/projects/status/github/mgedmin/profilehooks?branch=master&svg=true
   :target: https://ci.appveyor.com/project/mgedmin/profilehooks

.. image:: https://coveralls.io/repos/mgedmin/profilehooks/badge.svg?branch=master
   :target: https://coveralls.io/r/mgedmin/profilehooks


It's a collection of decorators for profiling functions.  E.g. to profile a
single function::

    from profilehooks import profile

    @profile
    def my_function(args, etc):
        pass

The results will be printed when the program exits (or you can use
``@profile(immediate=True)``).

If you're interested in coarse timings and don't want to pay for the overhead
of profiling, use ::

    from profilehooks import timecall

    @timecall       # or @timecall(immediate=True)
    def my_function(args, etc):
        pass

Finally, you may be interested in seeing line coverage for a single function ::

    from profilehooks import coverage

    @coverage
    def my_function(args, etc):
        pass

Also functions can be available in Python console or module if run it with -m arg ::

     $ python -m profilehooks
     >>> profile
     <function profile at 0x1005c6488>

     $ python -m profilehooks yourmodule

Full documentation is available through ``pydoc profilehooks`` after
installation.

The home page for this module is http://mg.pov.lt/profilehooks.  It has
screensho, uh, that is, more examples.
