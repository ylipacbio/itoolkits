type module >& /dev/null || . /mnt/software/Modules/current/init/bash

# This must come first so that everything else we add later
# will take precedence.
module load smrttools/incremental
which blasr
which pbindex
which pbdagcon

module load gcc/4.9.2
module load zlib

# For isolation:
export PYTHONUSERBASE=$(pwd)/LOCAL
mkdir -p LOCAL/

# We need pip.
export PATH=$PYTHONUSERBASE/bin:/mnt/software/a/anaconda2/4.2.0/bin:$PATH
which pip

THISDIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
echo THISDIR=$THISDIR
cd $THISDIR
# Everything else happens in THISDIR.
