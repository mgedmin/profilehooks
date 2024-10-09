#!/usr/bin/env python
import os

from setuptools import setup


here = os.path.dirname(__file__)


def read(filename):
    with open(os.path.join(here, filename)) as f:
        return f.read()


with open(os.path.join(here, 'profilehooks.py')) as f:
    for line in f:
        if line.startswith('__version__ = '):
            version = line.split(' = ')[1].strip('\'"\n')


setup(
    name='profilehooks',
    version=version,
    author='Marius Gedminas',
    author_email='marius@gedmin.as',
    url='https://mg.pov.lt/profilehooks/',
    description='Decorators for profiling/timing/tracing individual functions',
    long_description=read('README.rst') + '\n\n' + read('CHANGES.rst'),
    long_description_content_type='text/x-rst',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Programming Language :: Python :: 3.13',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
    ],
    python_requires=">=3.7",
    keywords='profile coverage decorators',
    license='MIT',

    py_modules=['profilehooks'],
    zip_safe=False,
)
