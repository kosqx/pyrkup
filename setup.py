#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import with_statement, division, absolute_import


import io
import codecs
import os
import sys
from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand


import pyrkup


class PyTest(TestCommand):
    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        import pytest
        errcode = pytest.main(self.test_args)
        sys.exit(errcode)


setup(
    name='pyrkup',
    version=pyrkup.__version__,
    url='http://github.com/kosqx/pyrkup/',
    license='BSD',
    author='Krzysztof Kosyl',
    tests_require=['pytest'],
    install_requires=[],
    cmdclass={'test': PyTest},
    author_email='krzysztof.kosyl@gmail.com',
    description='Converter between multiple markup formats',
    long_description='Converter between multiple markup formats',
    packages=['pyrkup'],
    include_package_data=True,
    platforms='any',
    test_suite='pyrkup.tests.test_pyrkup',
    classifiers = [
        'Programming Language :: Python',
        'Development Status :: 3 - Alpha',
        'Natural Language :: English',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Topic :: Software Development :: Documentation',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Text Processing :: Markup',
        'Topic :: Text Processing :: Markup :: HTML',
        ],
    extras_require={
        'testing': ['pytest'],
    }
)
