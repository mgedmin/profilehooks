profilehooks
============

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

Full documentation is available through ``pydoc profilehooks`` after
installation.

The home page for this module is http://mg.pov.lt/profilehooks.  It has
screensho, uh, that is, more examples.
