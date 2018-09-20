#!/usr/bin/env python
"""
Convert arbitrary dataset to datastore, and datastore to dataset
"""

from __future__ import absolute_import
import argparse
import sys
import logging
import os.path as op

FORMATTER = op.basename(__name__) + ':%(levelname)s:'+'%(message)s'
logging.basicConfig(level=logging.INFO, format=FORMATTER)
log = logging.getLogger(__name__)


def is_datastore(f):
    return f.endswith('.json')

def is_dataset(f):
    return f.endswith('.xml')

from pbcommand.models import get_scatter_pbparser, FileTypes
from pbcoretools.datastore_utils import datastore_to_datastorefile_objs, \
        dataset_to_datastore, ALLOWED_TYPES

def ds_to_ds(in_fn, out_fn):
    if is_datastore(in_fn) and is_dataset(out_fn):
        return datastore_to_dataset(in_fn, out_fn)
    elif is_dataset(in_fn) and is_datastore(out_fn):
        return dataset_to_datastore(in_fn, out_fn, __file__)
    else:
        raise ValueError("Can not convert {} to {}".format(in_fn, out_fn))


def datastore_to_dataset(in_fn, out_fn):
    objs, dataset_type_id, readcls, ext =  datastore_to_datastorefile_objs(
            in_fn, allowed_types=ALLOWED_TYPES)
    if not out_fn.endswith(ext):
        raise ValueError("Output file {} of type {} must ends with {}".format(
                          out_fn, dataset_type_id, ext))
    with readcls(*[f.path for f in objs], strict=True, skipCounts=True) as ds:
        ds.newUuid()
        ds.write(out_fn)

def run(args):
    log.info("locals: {!r}".format(locals()))
    ds_to_ds(args.in_fn, args.out_fn)


def get_parser():
    """Set up and return argument parser."""
    parser = argparse.ArgumentParser('dataset to datastore converters')
    parser.add_argument("in_fn", type=str, help="Input DataSet or DataStore")
    parser.add_argument("out_fn", type=str, help="Output DataSet or DataStore")
    return parser


def main(args=sys.argv[1:]):
    """main"""
    run(get_parser().parse_args(args))


if __name__ == "__main__":
    sys.exit(main(args=sys.argv[1:]))
