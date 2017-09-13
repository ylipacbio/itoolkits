#!/bin/bash -e
THISDIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
echo $THISDIR
set -vex
source $THISDIR/bamboo_setup.sh

## debug bamboo
ls -larth
bamboo_build_working_directory=${bamboo_build_working_directory:-$(pwd)}
rm -rf ${bamboo_build_working_directory}/test-reports
TRDIR=${bamboo_build_working_directory}/test-reports
mkdir ${TRDIR}

pip install --user coverage

make coverage-clean
make coverage-install

N="-v -s --durations=0 --junit-xml=${TRDIR}/pbtranscript2_integ.xml"
MY_NOSE_FLAGS=${N} make coverage-test

make coverage-report
