#!/usr/bin/env python

"""setup the python package.py"""

import subprocess
import os

__author__ = 'juan pablo isaza'

# create directory if missing
if 'dist' not in [x[0] for x in os.walk('.')]:
	create_subdirectory = 'mkdir dist'
	subprocess.call(create_subdirectory, shell=True, executable="/bin/bash")

empty_folder = 'rm dist/*'
subprocess.call(empty_folder, shell=True, executable="/bin/bash")

new_wheel = 'python setup.py sdist bdist_wheel'
subprocess.call(new_wheel, shell=True, executable="/bin/bash")

# Install twine first.
upload = 'twine upload dist/*'
subprocess.call(upload, shell=True, executable="/bin/bash")
