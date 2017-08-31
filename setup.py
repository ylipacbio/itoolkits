from setuptools import setup, find_packages
from distutils.extension import Extension
import os.path
import sys
import numpy

__author__ = "yli@pacificbiosciences.com"
version = "0.1.0"

if 'setuptools.extension' in sys.modules:
    m = sys.modules['setuptools.extension']
    m.Extension.__dict__ = m._Extension.__dict__


ext_modules = []

def _get_local_file(file_name):
    return os.path.join(os.path.dirname(__file__), file_name)


def _get_requirements(file_name):
    with open(file_name, 'r') as f:
        reqs = [line for line in f if not line.startswith("#")]
    return reqs


def _get_local_requirements(file_name):
    return _get_requirements(_get_local_file(file_name))


def run_cmd(cmd):
    import subprocess
    p = subprocess.Popen(cmd,
                         stdin=subprocess.PIPE,
                         stdout=subprocess.PIPE,
                         stderr=subprocess.STDOUT,
                         shell=True)
    return p.stdin, p.stdout

def check_program(program):
    import re
    try:
        stdin, stdout = run_cmd('/usr/bin/which "%s"||echo no' % program)
        lines = stdout.readlines()
        match = filter(lambda x: re.search(program, x), lines)
        if match:
            return True
        else:
            return False
    except (IndexError, ValueError, AttributeError):
        print >> sys.stderr, '%s is required, please install %s' % program
        return False


def exit_if_not_installed(program):
    if (not check_program(program=program)):
        print >> sys.stderr, 'Unable to install - %s must be installed and in the PATH variable' % program
        sys.exit(1)


if ("install" in sys.argv):
    exit_if_not_installed("blasr")

setup(
    setup_requires=['setuptools_cython'],
    name = 'itoolkits',
    version=version,
    author='Yuan Li',
    author_email='yli@pacificbiosciences.com',
    license='LICENSE.txt',
    ext_modules = ext_modules,
    include_dirs=[numpy.get_include()],
    scripts=['itoolkits/misc/consolidate-xml.py',
             'itoolkits/isoseq/subset_isoseq_subreads.py',
             'itoolkits/hgap/validate_smrtlink_hgap4.py',
             'itoolkits/misc/extract_seq_from_fasta.py'
            ],
    #entry_points={'console_scripts': [
    #    'pbtranscript = pbtranscript.PBTranscriptRunner:main',
    #    ]},
    package_dir={'itoolkits': 'itoolkits'},
    package_data={'itoolkits':
                  ['isoseq/isoseq_settings/isoseq_options.xml']},
    packages=find_packages(),
    zip_safe=False,
    install_requires=_get_local_requirements("REQUIREMENTS.txt")
)
