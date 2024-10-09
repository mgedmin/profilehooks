Changelog
=========

1.13.0 (2024-10-09)
-------------------

- Add support for Python 3.9, 3.10, 3.11, 3.12, and 3.13.

- Drop support for Python 2.7, 3.5 and 3.6.

- Drop support for ``hotshot`` (which was only available for Python 2.7).


1.12.0 (2020-08-20)
-------------------

- Added the ability to pass a text-mode file object to the ``stdout`` kwarg
  of the ``@profile()`` decorator and ``FuncProfiler()`` constructor for
  capturing output: https://github.com/mgedmin/profilehooks/pull/26.


1.11.2 (2020-03-03)
-------------------

- Fix breakage with ``@functools.lru_cache()``:
  https://github.com/mgedmin/profilehooks/issues/25.

- Use ``@functools.wraps()`` so decorated functions now correctly set the
  ``__wrapped__`` attribute.


1.11.1 (2020-01-30)
-------------------

- Add support for Python 3.8.

- Detect Python source file encoding correctly in ``@coverage``.
  https://github.com/mgedmin/profilehooks/issues/24.


1.11.0 (2019-04-23)
-------------------

- New options: ``@timecall(log_name='logger', log_level=DEBUG)``.
  https://github.com/mgedmin/profilehooks/pull/20.

- Add Python 3.7 support.

- Drop Python 3.3 and 3.4 support.


1.10.0 (2017-12-09)
-------------------

- ``@timecall()`` now defaults to the highest-precision timer
  (``timeit.default_timer()``) instead of ``time.time()``:
  https://github.com/mgedmin/profilehooks/pull/11


1.9.0 (2017-01-02)
------------------

- Drop claim of Python 3.2 compatibility.  Everything still works, except I'm
  no longer running automated tests on 3.2, so things might regress.

- Drop Python 2.6 compatibility.

- Add Python 3.6 compatibility.


1.8.1 (2015-11-21)
------------------

- Include PID in temporary filenames:
  https://github.com/mgedmin/profilehooks/issues/6.

- Claim Python 3.5 compatibility.


1.8.0 (2015-03-25)
------------------

- New option: ``@profile(stdout=False)`` to suppress output to sys.stdout.


1.7.1 (2014-12-02)
------------------

- Make ``@profile(profiler='hotshot')`` work again.  This was probably broken
  in 1.0 or 1.1, but nobody complained.

- Fix missing space in the output of ``@profile(skip=N)``.

- Make ``@coverage_with_hotshot`` output match ``@coverage`` output precisely.

- 100% test coverage.

- Claim Python 3.4 and PyPy compatibility.


1.7 (2013-10-16)
----------------

- Explicitly claim Python 3.3 compatibility.

- Fix Python 3.x bug with @coverage (stop using sys.maxint):
  https://github.com/mgedmin/profilehooks/issues/2.


1.6 (2012-06-05)
----------------

- Added Python 3.2 compatibility, dropped Python 2.3, 2.4 and 2.5 compatibility.

- Migrated the source repository to https://github.com/mgedmin/profilehooks

- Added a changelog.


1.5 (2010-08-13)
----------------

- New argument to @timecall: timer (defaults to time.time).
  Example: @timecall(timer=time.clock)

- Better documentation.


1.4 (2009-03-31)
----------------

- Added support for cProfile, make it the default profiler when available.
  Previously profilehooks supported profile and hotshot only.


1.3 (2008-06-10)
----------------

- Store profile results (when you pass filename to @profile) in pstats format
  instead of pickles.  Contributed by Florian Schulze.


1.2 (2008-03-07)
----------------

- New argument to: @timecall: immediate (defaults to False).

- Added a test suite.


1.1 (2007-11-07)
----------------

- First release to PyPI, with a setup.py and everything.

- New arguments to @profile: dirs, sort, entries.  Contributed by Hanno
  Schlichting.

- Preserve function attributes such as __doc__ and __module__ when decorating
  them.

- Pydoc-friendly docstring wrapping and other docstring improvements.


1.0 (2006-12-06)
----------------

- Changed licence from GPL to MIT.

- New decorator: @timecall

- New arguments to @profile: skip, filename, immediate.

- Added support for profile, after becoming convinced hotshot was unreliable.
  Made it the default profiler.


0.1 (2004-12-30)
----------------

- First public release (it didn't actually have a version number), announced on
  my blog: https://mg.pov.lt/blog/profiling.html

- @profile and @coverage decorators that didn't accept any arguments.

- hotshot was the only profiler supported for @profile, while @coverage used
  trace.py

