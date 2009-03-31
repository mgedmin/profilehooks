#!/usr/bin/env python
import os
from setuptools import setup

here = os.path.dirname(__file__)
long_description = open(os.path.join(here, 'README.txt')).read()

setup(
    name='profilehooks',
    version='1.4',
    author='Marius Gedminas',
    author_email='marius@gedmin.as',
    url='http://mg.pov.lt/profilehooks/',
    description='Decorators for profiling individual functions',
    long_description=long_description,
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
