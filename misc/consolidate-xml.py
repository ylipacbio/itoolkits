#!/usr/bin/env python
# consolidate-xml.py

from pbcore.io import ContigSet, FastaWriter
import argparser


def main(input_ds, output_fasta):
    """Convert input dataset to output fasta|fastq"""
    w = None
    if w.endswith(".fa") or w.endswith(".fasta"):
        w = FastaWriter(output_fasta)
        for r in ContigSet(input_ds):
            w.writeRecord(r)
        w.close()
    elif w.endswith(".fq") or w.endswith(".fastq"):
        w = FastqWriter(output_fasta)
        for r in ContigSet(input_ds):
            w.writeRecord(r)
        w.close()
    else:
        raise ValueError("output file must be either fasta or fastq")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print "Usage: %s input.xml output.fasta" % op.basename(__file__)
        sys.exit(1)

    sys.exit(main(input_ds=sys.argv[1], output_fasta=sys.argv[2])
