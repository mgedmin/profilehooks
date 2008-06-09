profilehooks
============

This is a module that helps you profile a single function (and all its callees)
by dropping in a decorator::

    from profilehooks import profile

    @profile
    def my_function(args, etc):
        pass

The documentation is available through ``pydoc profilehooks``.

The home page for this module is http://mg.pov.lt/profilehooks
