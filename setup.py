# -*- coding: UTF-8 -*-
#! /usr/bin/python

import sys
from setuptools import setup, find_packages

NAME    = 'vale'
VERSION = '0.1'
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
    long_description     = open('README.md').read(),
    author               = AUTHOR,
    author_email         = EMAIL,
    license              = LICENSE,
    keywords             = KEYWORDS,
    url                  = URL,
#    download_url     = URL+'/tarball/master',
)

# ...
packages = find_packages(exclude=["*.tests", "*.tests.*", "tests.*", "tests"])
# ...

def setup_package():
    if 'setuptools' in sys.modules:
        setup_args['install_requires'] = ['numpy']

    setup(  packages = packages \
          , include_package_data = True \
          , **setup_args)


if __name__ == "__main__":
    setup_package()
