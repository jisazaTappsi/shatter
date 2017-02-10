#!/usr/bin/env python

"""setup the python package.py"""

import os
from setuptools import setup
import setuptools
import pypandoc
from pip.req import parse_requirements

__author__ = 'juan pablo isaza'

# To publish do:
# $ python publish_update.py
# or execute manual commands.

# To add update requirements do:
# $ cd .. && pipreqs shatter/ --force

REQ = os.path.dirname(os.path.realpath(__file__))+"/requirements.txt"
install_requirements = parse_requirements(REQ, session=False)

# e.g. ['django==1.5.1', 'mezzanine==1.4.6']
requirements = [str(ir.req) for ir in install_requirements]

setup(
	name='shatter',
	version='0.5.3',
	author='Juan Pablo Isaza',
	author_email='biosolardecolombia@gmail.com',
	description='Data Driven Programming',
	long_description=pypandoc.convert('README.md', 'rst'),
	license=open("LICENSE.txt").read(),
	keywords='Quine McCluskey, Machine Learning, code, automatic code generation, expression',
	url='https://github.com/jisazaTappsi/shatter',
	packages=setuptools.find_packages(),
	classifiers=[
		'Development Status :: 3 - Alpha',
		'License :: OSI Approved :: MIT License',
		'Programming Language :: Python :: 3.6',
		'Intended Audience :: Developers',
		'Topic :: Software Development :: Build Tools',
	],
	install_requires=[requirements],
)
