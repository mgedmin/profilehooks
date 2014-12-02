#!/usr/bin/env python
import os
from setuptools import setup


here = os.path.dirname(__file__)


def read(filename):
    with open(os.path.join(here, filename)) as f:
        return f.read()


setup(
    name='profilehooks',
    version='1.7.1',
    author='Marius Gedminas',
    author_email='marius@gedmin.as',
    url='http://mg.pov.lt/profilehooks/',
    description='Decorators for profiling/timing/tracing individual functions',
    long_description=read('README.rst') + '\n\n' + read('CHANGES.rst'),
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
    ],
    license='MIT',

    py_modules=['profilehooks'],
    test_suite='test_profilehooks',
    zip_safe=False,
)
