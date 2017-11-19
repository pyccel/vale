# -*- coding: UTF-8 -*-
#! /usr/bin/python

import sys
from setuptools import setup, find_packages
import vale

NAME    = 'vale'
VERSION = vale.__version__
AUTHOR  = 'Ahmed Ratnani'
EMAIL   = 'ahmed.ratnani@ipp.mpg.de'
URL     = 'https://github.com/ratnania/vale'
DESCR   = 'a Domain Specific Language for Variational formulations.'
KEYWORDS = ['math']
LICENSE = "LICENSE"

setup_args = dict(
    name                 = NAME,
    version              = VERSION,
    description          = DESCR,
    long_description     = open('README.rst').read(),
    author               = AUTHOR,
    author_email         = EMAIL,
    license              = LICENSE,
    keywords             = KEYWORDS,
    url                  = URL,
)

# ...
packages = find_packages(exclude=["*.tests", "*.tests.*", "tests.*", "tests"])
# ...

# ...
install_requires = ['numpy', 'sympy']

try:
    import textx
except:
    install_requires += ['textx']
# ...

def setup_package():
    setup(packages=packages, \
          include_package_data=True, \
          zip_safe=True, \
          install_requires=install_requires, \
          **setup_args)

if __name__ == "__main__":
    setup_package()
