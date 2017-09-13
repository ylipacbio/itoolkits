import os
import sys
import re
import numpy
from setuptools import find_packages
from distutils.extension import Extension

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

version = __import__('mytool').get_version()

_REQUIREMENTS_FILE = 'REQUIREMENTS.txt'
_README = 'README.md'

if 'setuptools.extension' in sys.modules:
    m = sys.modules['setuptools.extension']
    m.Extension.__dict__ = m._Extension.__dict__


ext_modules = [ ]

def _get_local_file(file_name):
    return os.path.join(os.path.dirname(__file__), file_name)


def _get_description(file_name):
    with open(file_name, 'r') as f:
        _long_description = f.read()
    return _long_description


def _get_requirements(file_name):
    with open(file_name, 'r') as f:
        lines = f.readlines()
    rx = re.compile('^[A-z]')
    requirements = [l for l in lines if rx.match(l) is not None]
    return requirements

setup(
    setup_requires=['setuptools_cython'],
    name = 'mytool',
    version=version,
    author='Pacific Biosciences',
    author_email='etseng@pacb.com; cdunn@pacb.com; yli@pacb.com',
    license='LICENSE.txt',
    description='PacBio IsoSeq-2 tools.',
    ext_modules = ext_modules,
    include_dirs=[numpy.get_include()],
    scripts=[],
    entry_points={'console_scripts': [ ]},
    package_dir={'mytool': 'mytool'},
    package_data={'mytool': [ ]},
    packages=find_packages(),
    tests_require=['pytest'],
    long_description=_get_description(_get_local_file(_README)),
    classifiers=['Development Status :: 4 - Beta'],
    zip_safe=False,
    install_requires=_get_requirements(_get_local_file(_REQUIREMENTS_FILE))
)
