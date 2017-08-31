#!/usr/bin/env python

import sys
from pbsv.independent.FastaReader import read_fasta
from pbcore.io import FastaWriter
from argparse import ArgumentParser

def run(args):
    in_fa = args.input_fasta
    seq_to_extract = args.seq_to_extract
    out_fa = args.output_fasta

    writer = FastaWriter(out_fa)

    for r in read_fasta(open(in_fa, 'r')):
        if r[0].startswith(seq_to_extract):
            writer.writeRecord(r[0], r[1])


def get_parser():
    """Set up and return argument parser."""
    parser = ArgumentParser()
    parser.add_argument("input_fasta", help="Input fasta filename")
    parser.add_argument("seq_to_extract", help="Sequence to extract from filename")
    parser.add_argument("output_fasta", help="Output fasta filename")
    return parser



def main():
    """main"""
    sys.exit(run(get_parser().parse_args(sys.argv[1:])))

if __name__ == "__main__":
    main()
