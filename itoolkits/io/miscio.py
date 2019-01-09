#!/usr/bin/env python
import os.path as op
from pbcore.io import ContigSet, FastaWriter, FastqWriter

__all__ = ["smrtlink_dir", "consolidate_xml"]
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


def consolidate_xml(input_ds, out):
    """Convert input dataset to output fasta|fastq"""
    w = None
    if out.endswith(".fa") or out.endswith(".fasta"):
        w = FastaWriter(out)
        for r in ContigSet(input_ds):
            w.writeRecord(r)
        w.close()
    elif out.endswith(".fq") or out.endswith(".fastq"):
        w = FastqWriter(out)
        for r in ContigSet(input_ds):
            w.writeRecord(r)
        w.close()
    else:
        raise ValueError("output file must be either fasta or fastq")

