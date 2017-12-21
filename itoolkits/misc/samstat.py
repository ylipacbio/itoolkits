#!/usr/bin/env python

import sys
import pandas as pd
from argparse import ArgumentParser
from ..libs import AlignmentFile


def pct_similarity(r):
    if r.is_unmapped:
        return 'NA'
    match, insertion, deletion, skip, softclip, hard_clip, pad, equal, diff, back, nm =  r.get_cigar_stats()[0]
    return int(100 * (1.0 - nm * 2.0 / (2 * match + insertion + deletion)))


def samstat(bam_fn):
    """
    Return pandas dataframe of stats, including
      number of mapped, unmapped, supplementary, secondary
      aligned query start, aligned query read length, total query length,
      aligned target length, total target length, percentage similarity, mapQV
    """
    columns = ['IsMapped', 'IsSupplementary', 'IsSecondary',
               'QueryAlnStart', 'QueryAlnLength', 'QueryLength',
               'TargetAlnStart', 'TargetAlnLength',
               'PctSimilarity', 'MapQV']
    d = [(not r.is_unmapped, r.is_supplementary, r.is_duplicate,
          r.query_alignment_start, r.query_alignment_length, r.query_length,
          r.reference_start, r.reference_length,
          pct_similarity(r), r.mapping_quality) for r in AlignmentFile(bam_fn)]
    return pd.DataFrame(data=d, columns=columns)


def display_stat(stat):
    n_reads = len(stat) * 1.0
    mapped_stat = stat.loc[stat.IsMapped]
    def f(var):
        n = len(stat.loc[stat[var]])
        return '{}: num={}, percent={}'.format(var.ljust(30), n, n * 100.0 / n_reads)
    def g(var):
        d = mapped_stat[var]
        return '{}: mean={:.2f}, std={:.2f}, min={:.2f}, 25%={:.2f}, 50%={:.2f}, max={:.2f}'.format(var.ljust(30), d.mean(), d.std(), d.min(), d.quantile(0.25), d.quantile(0.50), d.max())
    content = [f('IsMapped'), f('IsSupplementary'), f('IsSecondary'),
               g('QueryAlnLength'), g('QueryLength'), g('TargetAlnLength'), g('PctSimilarity'), g('MapQV')]
    for c in content:
        print c


def run(args):
    stat = samstat(args.input_bam)
    display_stat(stat)


def get_parser():
    """Set up and return argument parser."""
    parser = ArgumentParser()
    parser.add_argument("input_bam", help="Input BAM/SAM filename")
    return parser

def main():
    """main"""
    sys.exit(run(get_parser().parse_args(sys.argv[1:])))

if __name__ == "__main__":
    main()
