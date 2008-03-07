#!/usr/bin/env python
from setuptools import setup

setup(
    name='profilehooks',
    version='1.2',
    author='Marius Gedminas',
    author_email='marius@gedmin.as',
    url='http://mg.pov.lt/profilehooks/',
    description='Decorators for profiling individual functions',
    classifiers = [
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Operating System :: OS Independent',
    ],
    license='MIT',

    py_modules=['profilehooks'],
    test_suite='test_profilehooks',
    zip_safe=False,
)
