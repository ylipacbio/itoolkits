# This script is designed to make a tiny test dataset from
# existing Iso-Seq datasets for quickly testing Iso-Seq pipeline.
#
# Input:
#     * a subreadset bam  -- containing reads of exactly one SMRTCells
#     * cluster_report.csv -- Iso-Seq ICE csv report
#     * hq_isoforms.fasta -- Iso-Seq polished HQ isoforms in FASTA
#     * lq_isoforms.fasta -- Iso-Seq polished LQ isoforms in FASTA
#     * num_hq_isoforms -- select reads associated with {num_hq_isoforms} HQ isoforms
#     * num_lq_isoforms -- select reads associated with {num_lq_isoforms} LQ isoforms
#
# Output:
#     * outdir/outprefix.zmw.txt -- a selected subset of zmws
#     * outdir/outprefix.subreads.bam/pbi/bai/xml -- subreads of selected zmws
#

#!/usr/bin/env python

import argparse
import itertools
import os.path as op
import numpy as np
from pbcore.io import FastaReader
from pbtranscript.Utils import mkdir, execute


def map_cluster_ids_to_zmw_ids(cluster_report_csv): # make sure exactly one smrtcell
    """
    Input: path to cluster report csv file
    Output: {cluster_id: set(zmw_ids)}

    Cluster report csv may look like:
         cluster_id,read_id,read_type
         i0_ICE_samplee049b6|c1,m54086_160831_230338/55706128/854_52_CCS,FL
         i0_ICE_samplee049b6|c1,m54086_160831_230338/10000000/0_800_CCS,FL

    Output:
         {i0_ICE_samplee049b6|c1: set(55706128, 10000000)}
    """
    c2z = {}
    movie = ""
    with open(cluster_report_csv, 'r') as reader:
        for line in reader:
            if line.strip() == "" or line.startswith("cluster_id"):
                continue
            c, z, t = line.split(',')
            c = c.split('/')[0] #i0_ICE_samplexxxx|c1 or i0_ICE_samplexxxx|c1/f3p10/1000
            if movie == "":
                movie = z.split('/')[0]
            else:
                assert movie == z.split('/')[0]
            z = int(z.split('/')[1]) # movie/zmw/s_e --> int(zmw)

            if c not in c2z:
                c2z[c] = set()
            c2z[c].update([z])

    #for k in c2z:
    #    print '%s --> %s' % (k, c2z[k])
    return c2z


def extract_subreads_by_zmw_ids(input_bam, output_bam, zmw_ids):
    """
    Write zmw ids to *.zmw.txt. Extact subreads of selected zmws
    from input_bam and write to output_bam, generate indices and
    make dataset xml.
    """
    # Write sorted zmw ids to *.zmw.txt
    zmw_ids_txt = output_bam[:-4] + ".zmw.txt"
    with open(zmw_ids_txt, 'w') as writer:
        for zmw_id in sorted(zmw_ids):
            writer.write("{zmw_id}\n".format(zmw_id=zmw_id))

    cmd = ['bamSieve', input_bam, output_bam, '--whitelist=%s' % zmw_ids_txt]
    print 'Running CMD: ' + ' '.join(cmd)
    execute(' '.join(cmd))

    # build index and make xml from output_bam
    output_xml = output_bam[:-4] + "et.xml"
    cmd = ['dataset', 'create', output_xml, output_bam, '--type=SubreadSet', '--generateIndices']
    print 'Running CMD: ' + ' '.join(cmd)
    execute(' '.join(cmd))

    print "Output selected zmw: %s" % zmw_ids_txt
    print "Output subreads bam: %s" % output_bam
    print "Output subreads xml: %s" % output_xml


def get_fasta_ids(fasta_file):
    """
    Returns all fasta ids in fasta_file as a list, e.x.,
        ['i1_HQ_samplee049b6|c0/f3p0/1801', 'i1_HQ_samplee049b6|c1/f3p10/1900']
    """
    return [r.name.split(' ')[0] for r in FastaReader(fasta_file)]

def get_hq_cluster_ids(fasta_file):
    """
    Gets a list of HQ cluster ids and converts to a list of ICE cluster ids, e.x.,

    HQ isoform ids look like:
        ['i1_HQ_samplee049b6|c0/f3p0/1801']
    return
        ['i1_ICE_samplee049b6|c0/f3p0/1801']
    """
    return [name.split('/')[0].replace('HQ', 'ICE') for name in get_fasta_ids(fasta_file)]

def get_lq_cluster_ids(fasta_file):
    """
    LQ isoform ids look like:
        ['i1_LQ_samplee049b6|c0/f3p0/1801']
    return
        ['i1_ICE_samplee049b6|c0/f3p0/1801']
    """
    return [name.split('/')[0].replace('LQ', 'ICE') for name in get_fasta_ids(fasta_file)]


def subset_isoseq_bam(input_bam, cluster_report_csv,
                      hq_isoforms_fasta, lq_isoforms_fasta,
                      outdir, outprefix, num_hq_isoforms, num_lq_isoforms,
                      random_seed=0):
    # make output dir
    mkdir(outdir)

    # map cluster ids to zmw ids from csv report
    c2z = map_cluster_ids_to_zmw_ids(cluster_report_csv) # make sure exactly one smrtcell

    # random select hq/lq isoform clusters
    np.random.seed(random_seed)
    hq_cluster_ids = np.random.choice(get_hq_cluster_ids(hq_isoforms_fasta), num_hq_isoforms)
    lq_cluster_ids = np.random.choice(get_lq_cluster_ids(lq_isoforms_fasta), num_lq_isoforms)
    print 'Selected hq isoforms are %s' % hq_cluster_ids
    print 'Selected lq isoforms are %s' % lq_cluster_ids

    # get zmws associated with selected isoform clusters and sort them
    hq_zmw_ids = set()
    for cid in hq_cluster_ids:
        for zmw_id in c2z[cid]:
            hq_zmw_ids.update([zmw_id])
    #print 'hq_zmw_ids = %s' % hq_zmw_ids

    lq_zmw_ids = set()
    for cid in lq_cluster_ids:
        for zmw_id in c2z[cid]:
            lq_zmw_ids.update([zmw_id])
    #print 'lq_zmw_ids = %s' % lq_zmw_ids

    zmw_ids = sorted([i for i in hq_zmw_ids.union(lq_zmw_ids)]) # sorted list of zmw ids
    print 'selected zmw ids are %s' % zmw_ids

    # extract subreads of selected zmws
    output_bam = op.join(outdir, outprefix+".subreads.bam")
    extract_subreads_by_zmw_ids(input_bam=input_bam, output_bam=output_bam, zmw_ids=zmw_ids)


def get_parser():
    """Get parser"""
    description = "Subset input bam by cherry-picking subreads which support a few HQ/LQ isoforms based on existing Iso-Seq analysis of the input bam."
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument("input_bam", type=str, help="Input subreads bam file")
    parser.add_argument("cluster_report_csv", type=str, help="cluster report csv output running Iso-Seq on input bam")
    parser.add_argument("hq_isoforms_fasta", type=str, help="HQ isoform fasta output running Iso-Seq on input bam")
    parser.add_argument("lq_isoforms_fasta", type=str, help="LQ isoform fasta output running Iso-Seq on input bam")
    parser.add_argument("outdir", type=str, help="Output directory")
    parser.add_argument("outprefix", type=str, help="Output file prefix")
    parser.add_argument("--num_hq_isoforms", type=int, default=1, help="Number of HQ isoforms selected")
    parser.add_argument("--num_lq_isoforms", type=int, default=1, help="Number of LQ isoforms selected")
    parser.add_argument("--random_seed", type=int, default=0, help="random number seed")

    return parser

if __name__ == "__main__":
    parser = get_parser()
    args = parser.parse_args()
    subset_isoseq_bam(input_bam=args.input_bam, cluster_report_csv=args.cluster_report_csv,
                      hq_isoforms_fasta=args.hq_isoforms_fasta, lq_isoforms_fasta=args.lq_isoforms_fasta,
                      outdir=args.outdir, outprefix=args.outprefix,
                      num_hq_isoforms=args.num_hq_isoforms, num_lq_isoforms=args.num_lq_isoforms,
                      random_seed=args.random_seed)

# E.x.
# python subset_isoseq_subreads.py \
# /pbi/collections/315/3150353/r54086_20160831_010819/4_D01/m54086_160831_230338.subreads.bam \
# cluster_report.csv hq_isoforms.fasta, lq_isoforms.fasta outdir outprefix \
# --num_hq_isoforms=3 --num_lq_isoforms=2 --random_seed=1
