__author__ = 'juan pablo isaza'

from setuptools import setup
import setuptools
import pypandoc

setup(
    name='Boolean Solver',
    version='0.1.11',
    author='Juan Pablo Isaza',
    author_email='biosolardecolombia@gmail.com',
    description='Fast development with generated boolean expressions.',
    long_description=pypandoc.convert('README.md', 'rst'),
    license='MIT',
    keywords='Quine McCluskey, Boolean, code, automatic code generation, expression, Boolean expression',
    url='https://github.com/jisazaTappsi/BooleanSolver',
    packages=setuptools.find_packages(),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
    ],
    install_requires=[],
)