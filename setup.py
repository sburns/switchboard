#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" setup.py

Packaging
"""
__author__ = 'Scott Burns <scott.s.burns@vanderbilt.edu>'
__copyright__ = 'Copyright 2013 Vanderbilt University. All Rights Reserved'

from switchboard import __version__ as VERSION
from setuptools import setup, find_packages

if __name__ == '__main__':

    setup(name='switchboard',
          version=VERSION,
          description="A small flask blueprint for accepting and delegating"
                      "REDCap Data Entry Triggers",
          author="Scott S Burns",
          author_email="scott.s.burns@vanderbilt.edu",
          packages=find_packages(),
          package_data={},
          classifiers=[
                # "Development Status :: 1 - Planning",
                # "Development Status :: 2 - Pre-Alpha",
                "Development Status :: 3 - Alpha",
                # "Development Status :: 4 - Beta",
                # "Development Status :: 5 - Production/Stable",
                # "Development Status :: 6 - Mature",
                # "Development Status :: 7 - Inactive",
                "Environment :: Console",
                "Environment :: Web Environment",
                "Intended Audience :: Developers",
                "Intended Audience :: Science/Research",
                "License :: OSI Approved :: BSD License",
                "Operating System :: MacOS :: MacOS X",
                "Operating System :: POSIX",
                "Operating System :: POSIX :: Linux",
                "Operating System :: Unix",
                "Programming Language :: Python :: 2.6",
                "Programming Language :: Python :: 2.7",
                "Programming Language :: Python :: 2 :: Only",
                "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
                "Topic :: Scientific/Engineering",
                "Topic :: Scientific/Engineering :: Information Analysis",
                ],
        )
