#!/usr/bin/env python
# consolidate-xml.py

import sys
from itoolkits import consolidate_xml


def main(input_ds, out):
    """Convert input dataset to output fasta|fastq"""
    consolidate_xml(input_ds, out)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print "Usage: %s input.xml output.fasta|fastq" % op.basename(__file__)
        sys.exit(1)

    sys.exit(main(input_ds=sys.argv[1], out=sys.argv[2]))
