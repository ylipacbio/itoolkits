#!/usr/bin/env python

"""Given a subreads.bam (and a scraps.bam), plot
x axis = unrolled polymerase read length
y axis = total subreads length
"""
import os.path as op
import numpy as np
import random
from collections import defaultdict
from pbcore.io import IndexedBamReader, SubreadSet
from pbtranscript.Utils import execute, realpath

#from PRmm.io import ZmwReadStitcher
#def get_lengths(sr_fn, sc_fn=None):
#    """
#    Return (unrolled_lens, mean_subread_lens)
#    """
#    if sc_fn is None:
#        sc_fn = sr_fn.replace(".subreads.bam", ".scraps.bam")
#
#    if not op.exists(sr_fn) or not op.exists(sc_fn):
#        raise IOError("%s and %s must exist!")
#
# ZmwStitcher is way too slow, just make the unrolled polymerase bam instead
#    unrolled_lens = []
#    mean_sr_lens = []
#    reader = ZmwReadStitcher(sr_fn, sc_fn)
#    asz = reader.allSequencingZmws
#    n = len(asz) # number of sequencing zmws which have basecalls
#    for i in range(0, n):
#        stitched_zmw = reader[asz[i]]
#        if len(stitched_zmw.subreads) != 0: # if has subreads
#            srs = stitched_zmw.subreads
#            sr_lens = [r.readEnd - r.readStart for r in srs]
#            mean_sr_lens.append(np.mean(sr_lens))
#            unrolled_lens.append(stitched_zmw.zmwReadLength)


def get_lengths(ds_fn):
    """
    Return (unrolled_read_lengths, total_subread_lengths)
    """
    print ds_fn

    assert op.exists(ds_fn)
    ds = SubreadSet(ds_fn)

    unrolled_lens_dict = defaultdict(int) # zmw --> approximated unrolled read length
    sr_lens_dict = defaultdict(list) # zmw --> list of subreads lengths
    for rr in ds.resourceReaders():
        for zmw, qEnd, qStart in zip(rr.holeNumber, rr.qEnd, rr.qStart):
            unrolled_lens_dict[zmw] = max(unrolled_lens_dict[zmw], qEnd)
            sr_lens_dict[zmw].append(qEnd - qStart)

    unrolled_lens = []
    total_sr_lens = []
    for zmw in sorted(unrolled_lens_dict.keys()):
        assert zmw in sr_lens_dict
        unrolled_lens.append(unrolled_lens_dict[zmw])
        total_sr_lens.append(sum(sr_lens_dict[zmw]))

    return (sorted(unrolled_lens_dict.keys()), unrolled_lens, total_sr_lens)


def dump_dat(dat, column_names, dump_fn):
    """
    Dump dat to dump file, always with header.
    dat[0,0], dat[0,1], dat[0,2]
    dat[1,0], dat[1,1], dat[1,2]
    dat[2,0], dat[2,1], dat[2,2]
    """
    with open(dump_fn, 'w') as writer:
        writer.write(",".join(column_names) + "\n")
        for d in dat:
            assert len(d) == len(column_names)
            writer.write(",".join([str(item) for item in d]) + "\n")


def write_R_code_4_dotplot(dat_fn, xvar, yvar, xlab, ylab, r_code_fn, plot_fn, plot_title="Main title"):
    """
    """
    stuff = ["""dat = read.csv("{dat_fn}", header=TRUE)""".format(dat_fn=realpath(dat_fn)),
             """jpeg("{plot_fn}")""".format(plot_fn=plot_fn),
             """dotchart(dat${x}, dat${y}, color="blue", xlab="{xlab}", ylab="{ylab}", main="{plot_title}")""".format(x=xvar, y=yvar, xlab=xlab, ylab=ylab, plot_title=plot_title),
             "dev.off()"]

    with open(r_code_fn, 'w') as writer:
        writer.write("\n".join(stuff))


def smrtlink_dir(smrtlink_host, job_id):
    """Given smrtlink host and job id, return path to a smrtlink job dir."""
    host_jobs_root = ""
    if smrtlink_host == "alpha":
        host_jobs_root = "/pbi/dept/secondary/siv/smrtlink/smrtlink-alpha/jobs-root/"
    elif smrtlink_host == "beta":
        host_jobs_root = "/pbi/dept/secondary/siv/smrtlink/smrtlink-beta/jobs-root/"
    else:
        raise ValueError("SMRTLink host %s is not supported." % smrtlink_host)

    return op.join(host_jobs_root,
            "{0:03d}".format(int(int(job_id)/1000)),
            "{0:06d}".format(int(job_id)))


def get_ds_fn(job_dir):
    """
    """
    with open(op.join(job_dir, "job.stdout"), 'r') as reader:
        for line in reader:
            if "\'eid_subread\':" in line:
                return line.split(':')[1].translate(None, ':, {}\'').strip()
    raise AssertionError


if __name__ == "__main__":
    #sr_fn = "/pbi/collections/319/3190034/r54029_20161012_005331/4_D01/m54029_161012_180811.subreads.bam"
    job_id = 1183
    host = "alpha"
    job_dir = smrtlink_dir(smrtlink_host=host, job_id=job_id)
    ds_fn = get_ds_fn(job_dir)
    #ds_fn = "/pbi/collections/319/3190034/r54029_20161012_005331/4_D01/m54029_161012_180811.subreadset.xml"
    print ds_fn

    UNROLLED_LEN, TOTAL_SR_LEN = "Unrolled Read Length", "Total Subread Length"
    plot_fn = "unrolled_len_vs_total_sr_len.jpg"

    # Define intermediate files
    prefix = "tmp." + str(random.randint(0, 1000000))
    dump_fn = prefix + ".dump.csv"
    r_code_fn = prefix + ".dotplot.R"

    zmws, unrolled_lens, total_sr_lens = get_lengths(ds_fn)
    xvar, yvar = 'unrolled_len','total_sr_len'
    dump_dat(dat=zip(zmws, unrolled_lens, total_sr_lens), dump_fn=dump_fn, column_names=('zmw', xvar, yvar))
    write_R_code_4_dotplot(dat_fn=dump_fn, xvar=xvar, yvar=yvar, xlab=UNROLLED_LEN, ylab=TOTAL_SR_LEN,
                           r_code_fn=r_code_fn, plot_fn=plot_fn, plot_title=str(job_id))
    #execute("Rscript {r_code_fn}".format(r_code_fn=r_code_fn))

    print dump_fn
    print r_code_fn
    #rm(r_code_fn)
    #rm(dump_fn)

