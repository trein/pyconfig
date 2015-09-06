#!/usr/bin/env python

from setuptools import setup


setup(name='pyconfig',
      version='0.1.0',
      description='Unified development workflow automation tool',
      author='Guilherme Trein',
      author_email='guitrein@yahoo.com.br',
      url='https://github.com/trein/pyconfig',
      license='Apache License 2.0',
      long_description=open('README.md').read(),
      platforms='all',
      install_requires=['virtualenv==13.1.2'],
      packages=['pyconfig'])