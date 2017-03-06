#!/usr/bin/env python

"""Make a subreads.bam and subreadset.xml containing
all reads in fasta file.
Input: a fasta file, a fofn of all subreads.bam files
Output: o.subreads.bam and o.subreadset.xml
"""
import sys
import argparse
from collections import defaultdict
import os.path as op
from pbcore.io import FastaReader
from pbtranscript.Utils import rmpath, execute


def get_parser():
    p = argparse.ArgumentParser(description="""Make a subreads.bam/xml containing all reads of a fasta file""")
    p.add_argument("in_fasta", help="Input FASTA file")
    p.add_argument("in_bam_fofn", help="Input BAM fofn")
    p.add_argument("out_prefix", help="Output prefix")
    p.add_argument("--dry_run", default=False, action="store_true", help="Dry run")
    return p

def get_zmws_in_fasta(in_fasta):
    """Return zmws {movie: set(zmws)} of reads in fasta"""
    movie_zmws = defaultdict(lambda: set()) #movie --> set of zmws
    for r in FastaReader(in_fasta):
        try:
            movie, zmw, dummy = r.name.split(' ')[0].split('/')
            zmw = int(zmw)
            movie_zmws[movie].add(zmw)
        except ValueError:
            raise ValueError("Read %r is not a PacBio read." % r.name)
    return movie_zmws


def run(args):
    out_prefix = args.out_prefix
    exts = ['.subreadset.xml', '.subreads.bam', '.xml', '.bam']
    for ext in exts:
        if out_prefix.endswith(ext):
            out_prefix = out_prefix[:-len(ext)]
            break

    make_subreads_bam_from_fasta(in_fasta=args.in_fasta, in_bam_fofn=args.in_bam_fofn, out_prefix=out_prefix, dry_run=args.dry_run)
    return 0

def get_movies_in_fofn(in_bam_fofn):
    movies_in_fofn = defaultdict(lambda: set())
    for fn in open(in_bam_fofn, 'r'):
        fn = fn.strip()
        if len(fn) == 0 or fn[0] == '#':
            continue
        movie = fn.split('/')[-1].split('.')[0]
        print "movie=%s" % movie
        movies_in_fofn[movie].add(fn)
    return movies_in_fofn


def make_subreads_bam_from_fasta(in_fasta, in_bam_fofn, out_prefix, dry_run=False):
    movie_zmws = get_zmws_in_fasta(in_fasta)
    movies_in_fofn = get_movies_in_fofn(in_bam_fofn)
    out_bam = out_prefix + '.subreads.bam'
    out_xml = out_prefix + '.subreadset.xml'
    rmpath(out_xml)
    rmpath(out_bam)

    out_bams = []
    for movie, zmws in movie_zmws.iteritems():
        in_subreads_bam_files = list(movies_in_fofn[movie])
        wl = ','.join([str(r) for r in list(zmws)])
        for in_subreads_bam in in_subreads_bam_files:
            tmp_out_bam = out_prefix + '.' + op.basename(in_subreads_bam) + ".subset.out.bam"
            cmd = "bamSieve {in_subreads_bam} {out_bam} --whitelist {wl}".format(in_subreads_bam=in_subreads_bam, out_bam=tmp_out_bam, wl=wl)
            print 'CMD: \n%s\n' % cmd
            if not dry_run:
                execute(cmd)
            out_bams.append(tmp_out_bam)

    # merge
    merged_xml = out_prefix + '.merged.xml'
    cmd = 'dataset merge {out_xml} {in_xmls}'.format(out_xml=merged_xml, in_xmls=' '.join(out_bams))
    print 'CMD: %s' % cmd
    if not dry_run:
        execute(cmd)

    cmd = 'dataset consolidate {in_xml} {out_bam} {out_xml}'.format(in_xml=merged_xml, out_bam=out_bam, out_xml=out_xml)
    print 'CMD: %s' % cmd
    if not dry_run:
        execute(cmd)

    rmpath(merged_xml)
    for fn in out_bams:
        rmpath(fn)
        rmpath(fn+'.pbi')

    if not op.exists(out_xml):
        raise ValueError("%s does not exist" % out_xml)
    if not op.exists(out_bam):
        raise ValueError("%s does not exist" % out_bam)


if __name__ == "__main__":
    sys.exit(run(get_parser().parse_args(sys.argv[1:])))

