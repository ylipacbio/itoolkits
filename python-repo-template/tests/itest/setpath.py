#!/usr/bin/python
from os import path
import ConfigParser

"""Define test data path for mytool."""

THIS_DIR = path.dirname(path.abspath(path.realpath(__file__)))
ROOT_DIR = path.dirname(THIS_DIR)
NOSE_CFG = path.join(THIS_DIR, "nose.cfg")

def _get_data_std_dir():
    """Get the data directory which contains all the unittests files.
    """
    nosecfg = ConfigParser.SafeConfigParser()
    nosecfg.readfp(open(NOSE_CFG), 'r')
    if nosecfg.has_section('data'):
        data_dir = path.join(THIS_DIR, nosecfg.get('data', 'dataDir'))
        siv_dir = path.abspath(nosecfg.get('data', 'sivDir'))
        return path.abspath(data_dir), path.abspath(siv_dir)
    else:
        msg = "Unable to find section [DATA] option [dataDir]" + \
              "and [sivDir] in config file {f}.".format(f=NOSE_CFG)
        raise KeyError(msg)

DATA_DIR, SIV_DIR = _get_data_std_dir()
OUT_DIR = path.join(THIS_DIR, "../out")
SIV_DAT_DIR = path.join(SIV_DIR, 'data')
