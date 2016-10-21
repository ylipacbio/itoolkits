#!/usr/bin/env python
# consolidate-xml.py

import sys
from pbcore.io import ContigSet, FastaWriter


def main(input_ds, out):
    """Convert input dataset to output fasta|fastq"""
    w = None
    if out.endswith(".fa") or out.endswith(".fasta"):
        w = FastaWriter(out)
        for r in ContigSet(input_ds):
            w.writeRecord(r)
        w.close()
    elif out.endswith(".fq") or out.endswith(".fastq"):
        w = FastqWriter(output_fasta)
        for r in ContigSet(input_ds):
            w.writeRecord(r)
        w.close()
    else:
        raise ValueError("output file must be either fasta or fastq")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print "Usage: %s input.xml output.fasta|fastq" % op.basename(__file__)
        sys.exit(1)

    sys.exit(main(input_ds=sys.argv[1], out=sys.argv[2]))
