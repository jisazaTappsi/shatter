__author__ = 'juan pablo isaza'

import subprocess

# To publish do:
# Empty dist folder
# $ python setup.py sdist bdist_wheel
# $ twine upload dist/*

empty_folder = 'rm dist/*'
subprocess.call(empty_folder, shell=True, executable="/bin/bash")

new_wheel = 'python setup.py sdist bdist_wheel'
subprocess.call(new_wheel, shell=True, executable="/bin/bash")

# Install twine first.
upload = 'twine upload dist/*'
subprocess.call(upload, shell=True, executable="/bin/bash")