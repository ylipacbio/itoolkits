#!/bin/bash -e
THISDIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
set -vex
source $THISDIR/bamboo_setup.sh

# debug bamboo
ls -larth
ls -larth $THISDIR/..
which python

# If .pyc exists from previous run, and if files have moved, tests can fail.
find pbtranscript2tools -name '*.pyc' | xargs rm -f

# Test just the completely indendent stuff first, without even installing.
make test-fast

# Reinvent the wheel (7s -- turn back on someday maybe)
#python setup.py bdist_wheel
# (goes into ./dist/)
# (not needed yet, but a useful quick check)

WHEELHOUSE=/home/cdunn/wheelhouse/glibc-2.12


# Build with dependencies (fairly fast)

#pip --no-cache-dir install ... ?

ZLIB_CFLAGS=$(pkg-config zlib --cflags)
ZLIB_LIBS=$(pkg-config zlib --libs)
HTSLIB_CONFIGURE_OPTIONS="--disable-libcurl --disable-bz2 --disable-lzma" \
  CFLAGS="-D_GNU_SOURCE ${ZLIB_CFLAGS}" \
  LDFLAGS="${ZLIB_LIBS}" \
  pip install -v --user --find-links=${WHEELHOUSE} --no-index 'pysam'
#  pip install -v --user 'pysam==0.9.1.4'
python -c 'import pysam.version; print pysam.version.__version__'
python -c 'import pysam.cfaidx; print pysam.cfaidx' || python -c 'import pysam.libcfaidx; print pysam.libcfaidx'

if [ -e $THISDIR/../pbcore ] ; then
    pushd ../pbcore
    pip install -v --user --find-links=${WHEELHOUSE} --no-index --edit .
    popd
else
    pip install -v --user --find-links=${WHEELHOUSE} --no-index pbcore
fi

# Drop --no-index, in case we are missing something.
pip install -v --user --find-links=${WHEELHOUSE} --edit .

which py.test || pip install --user pytest
#pip install -v --user pylint==1.7.1 && which pylint && pylint --version

which pbtranscript2 || ( pushd ../pbtranscript2 && pip install -v --user --edit . && popd && which pbtranscript2 )

make doctest
# Maybe turn these back on someday.
make pylint
