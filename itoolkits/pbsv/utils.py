#!/usr/bin/env python

"""
Define utils used in
* make-subreads-bam-from-fasta.py
* make-subreads-bam-from-zmws.py
"""
from collections import defaultdict
import os.path as op
from pbcore.io import FastaReader
from pbtranscript.Utils import rmpath, execute



def get_movie_and_zmw_from_name(name):
    """Given a string of pacbio zmw name or read name, return movie and zmw"""
    try:
        fs = name.strip().split(' ')[0].split('/')
        movie, zmw = fs[0], fs[1]
        return movie, int(zmw)
    except ValueError:
        raise ValueError("Read %r is not a PacBio read." % name)


def get_movie2zmws_in_txt(in_txt):
    """Return movie2zmws {movie: set(zmws)} of zmws or reads in txt"""
    movie2zmws = defaultdict(set()) #movie --> set of zmws
    for name in open(in_txt, 'r'):
        movie, zmw = get_movie_and_zmw_from_name(name)
        movie2zmws[movie].add(zmw)
    return movie2zmws


def get_movie2zmws_in_fasta(in_fasta):
    """Return movie2zmws {movie: set(zmws)} of reads in fasta"""
    movie2zmws = defaultdict(set()) #movie --> set of zmws
    for r in FastaReader(in_fasta):
        movie, zmw = get_movie_and_zmw_from_name(r.name)
        movie2zmws[movie].add(zmw)
    return movie2zmws


def fofn2fns(i_fofn):
    """Get filenames from fofn"""
    fns = []
    for fn in open(i_fofn, 'r'):
        fn = fn.strip()
        if len(fn) == 0 or fn[0] == '#':
            continue
        fns.append(fn)
    return fns


def get_movie2bams_from_fofn(in_bam_fofn):
    """
    Return {movie: bam}
    e.g.,
    if inpupt bam fofn has two bam files of two movies:
    movie1.subreads.bam
    movie2.subreads.bam
    return {'movie1': 'movie1.subreads.bam', 'movie2': 'movie2.subreads.bam'}
    e.g., if input bam fofn has two bam files of the same movie
    movie.1.subreads.bam
    movie.2.subreads.bam
    return {'movie': ['movie.1.subreads.bam', 'movie2.subreads.bam']}
    """
    movie2bams = defaultdict(set())
    for fn in fofn2fns(in_bam_fofn):
        movie = fn.split('/')[-1].split('.')[0]
        print "movie=%s" % movie
        movie2bams[movie].add(fn)
    return movie2bams


def rmpath_cmd(path):
    """rm a file path, not directory, command"""
    return 'rm -f %s' % path

def merge_bam2xml_cmd(in_bams, out_xml):
    """Merge bam files to xml command """
    cmd = 'dataset merge {out_xml} {in_bams}'.format(out_xml=out_xml, in_bams=' '.join(in_bams))
    return cmd

def consolidate_xml2bam_cmd(in_xml, out_bam, out_xml):
    """Consolidate in_xml to out_bam"""
    cmd = 'dataset consolidate {in_xml} {out_bam} {out_xml}'.format(in_xml=in_xml, out_bam=out_bam, out_xml=out_xml)
    return cmd


def bamsieve_zmw_subreads_cmd(in_subreads_bam, zmws, out_prefix):
    """in_subreads_bam -- input original subreads.bam, from which subreads will be extracted
    zmws -- a list of zmws
    out_prefix -- output prefix
    Return output (cmd, bam)
    """
    assert isinstance(zmws, list)
    wl = ','.join([str(r) for r in list(zmws)])
    out_bam = out_prefix + '.' + op.basename(in_subreads_bam) + ".subset.out.bam"
    cmd = "bamSieve {in_subreads_bam} {out_bam} --whitelist {wl}".format(in_subreads_bam=in_subreads_bam, out_bam=out_bam, wl=wl)
    return cmd, out_bam


def bamsieve_zmw_subreads_cmds(bam2zmws, out_prefix):
    """
    bam2zmws --> {subreads.bam: zmws},
    mapping a subreads.bam file to its white list zmws which will be extracted
    return cmds, out_bams
    """
    cmds, out_bams = [], []
    for in_bam, zmws in bam2zmws:
        cmd, out_bam = bamsieve_zmw_subreads_cmd(in_bam, zmws, out_prefix)
        cmds.append(cmd)
        out_bams.append(out_bam)
    return cmds, out_bams


def get_bam2zmws(movie2zmws, movie2bams):
    """
    movie2zmws --> {movie: zmws}
    movie2bams --> {movie: bam_files}  # allow *.1.subreads.bam, *.2.subreads.bam
    return bam2zmws{bam: zmws}
    e.g.,
    movie2zmws {'movie': [20,21,31]},
    movie2bams {'movie': ['movie.1.subreads.bam', 'movie.2.subreads.bam']}
    return bam2zmws{'movie.1.subreads.bam': [20,21,31], 'movie.2.subreads.bam': [20,21,31]}
    """
    bam2zmws = {}
    for movie, zmws in movie2zmws.iteritems():
        in_subreads_bam_files = list(movie2bams[movie])
        for in_subreads_bam in in_subreads_bam_files:
            bam2zmws[in_subreads_bam] = zmws
    return bam2zmws

def execute_cmds(cmds, dry_run):
    """Execute cmds if not dry_run, otherwise,print cmds"""
    print 'CMDs:\n%r\n' % ('\n'.join(cmds))
    if not dry_run:
        for cmd in cmd:
            execute(cmd)

def make_subreads_bam(movie2zmws, movie2bams, out_prefix, dry_run=False):
    """
    movie2zmws --> {movie: [zmw1,zmw2,..]}
    movie2bams --> {movie: [bam1,bam2,..]}
    out_prefix string, e.g., myout
    """
    out_bam = out_prefix + '.subreads.bam'
    out_xml = out_prefix + '.subreadset.xml'
    merged_xml = out_prefix + '.merged.xml'

    # map every bam file to its associated white list zmws
    bam2zmws = get_bam2zmws(movie2zmws=movie2zmws, movie2bams=movie2bams)

    c0 = rmpath_cmd(out_xml)
    c1 = rmpath_cmd(out_bam) # clean up before start

    _cmds, out_bams = bamsieve_zmw_subreads_cmds(bam2zmws=bam2zmws, out_prefix=out_prefix) # bamsieve cmds

    c2 = merge_bam2xml_cmd(in_bams=out_bams, out_xml=merged_xml) # merge cmd
    c3 = consolidate_xml2bam_cmd(in_xml=merged_xml, out_bam=out_bam, out_xml=out_xml) # consolidate cmd
    c4 = rmpath_cmd(merged_xml)

    cmds = [c0, c1] + _cmds + [c2, c3, c4]

    for fn in out_bams:
        cmds.extend([rmpath(fn), rmpath(fn+'.pbi')])

    execute_cmds(cmds=cmds, dry_run=dry_run)

    if not op.exists(out_xml):
        raise ValueError("%s does not exist" % out_xml)
    if not op.exists(out_bam):
        raise ValueError("%s does not exist" % out_bam)
