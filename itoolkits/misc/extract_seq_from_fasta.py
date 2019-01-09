#!/usr/bin/env python

import sys
from argparse import ArgumentParser
from itoolkits.misc.utils import  extract_a_fasta_record

def run(args):
    in_fa = args.input_fasta
    seq_to_extract = args.seq_to_extract
    out_fa = args.output_fasta

    extract_a_fasta_record(in_fa, out_fa, seq_to_extract)


def get_parser():
    """Set up and return argument parser."""
    parser = ArgumentParser()
    parser.add_argument("input_fasta", help="Input fasta filename")
    parser.add_argument("seq_to_extract", help="The only one sequence to extract from filename")
    parser.add_argument("output_fasta", help="Output fasta filename")
    return parser

def main():
    """main"""
    sys.exit(run(get_parser().parse_args(sys.argv[1:])))

if __name__ == "__main__":
    main()
