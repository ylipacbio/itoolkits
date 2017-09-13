import unittest
import os.path as op
from .setpath import DATA_DIR, OUT_DIR, SIV_DAT_DIR, OUT_DIR, SIV_DAT_DIR

def test_setup():
    for f in []:
        assert op.exists(f)
