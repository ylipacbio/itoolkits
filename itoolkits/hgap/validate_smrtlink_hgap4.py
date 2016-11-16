#!/usr/bin/env python
"""
Validate hgap4 outputs and get running time of tasks.
"""
import os.path as op
import sys
import time
import datetime
import argparse
import logging
from pbcore.util.Process import backticks
from pbtranscript.Utils import realpath, ln, mkdir
from itoolkits.io import consolidate_xml, smrtlink_dir


FORMATTER = op.basename(__file__) + ':%(levelname)s:'+'%(message)s'
logging.basicConfig(level=logging.DEBUG, format=FORMATTER)
log = logging.getLogger(__name__)


class SMRTLink_Job(object):
    """
    A SMRTLink job
    """
    def __init__(self, root_dir):
        self.root_dir = realpath(root_dir)

    @property
    def tasks_dir(self):
        """Return ${root_dir}/tasks"""
        return op.join(self.root_dir, "tasks")


class SMRTLink_HGAP4(SMRTLink_Job):
    """
    A SMRTLink HGAP4 job
    """
    def __init__(self, root_dir):
        super(SMRTLink_HGAP4, self).__init__(root_dir=root_dir)

    @property
    def polished_p_ctg_ds(self):
        """Return arrow/quiver output: polished contigs in fasta"""
        return op.join(self.tasks_dir, "pbcoretools.tasks.gather_contigset-1/file.contigset.xml")

    @property
    def p_ctg_fa(self):
        """return falcon final output p_ctg.fa"""
        return op.join(self.tasks_dir, "falcon_ns.tasks.task_falcon2_run_asm-0/p_ctg.fa")

    def make_links(self, out_dir):
        """
        Make file links or consolidate xml files to fasta
        """
        out_dir = realpath(out_dir)
        mkdir(out_dir)
        o_polished_ctg_fa = op.join(out_dir, "polished_p_ctg.fasta")
        log.info("Making polished p_ctg fasta: %s", o_polished_ctg_fa)
        consolidate_xml(self.polished_p_ctg_ds, o_polished_ctg_fa)

        def _ln_f(src):
            dst = op.join(out_dir, op.basename(src))
            log.info("Making %s", dst)
            ln(src, dst)
        _ln_f(self.p_ctg_fa)

    def task_dirs(self, task):
        """If input task is scatter-able, return working directories of
        scattered tasks. Otherwise, return working directories of the only task.
        """
        ret = []
        if op.exists(op.join(self.tasks_dir, task + "-0")):
            # This task is not scatter-able
            ret = [op.join(self.tasks_dir, task + "-0")]
        else:
            for i in range(1, 10000):
                s_task_dir = op.join(self.tasks_dir, task + "-" + str(i))
                if op.exists(s_task_dir):
                    ret.append(s_task_dir)
                else:
                    break
        if len(ret) == 0:
            raise IOError("Could not find task %s/%s" % (self.tasks_dir, task))
        return ret

    def _get_time_from_line(self, line):
        """Input line should be of format:
        *[${log_level}] yyyy-mm-dd hh:mm:ss,?z [pbcommand.*] Loading pbcommand *
        *[${log_level}] yyyy-mm-dd hh:mm:ss,?z [pbcommand.*] Completed running *

        e.g.,
        *[INFO] 2016-09-20 18:15:42,873z [pbcommand.cli.quick _w 245] Loading pbcommand *
        *[ERROR] 2016-09-20 18:15:42,873z [pbcommand.cli.quick _w 245] Completed running *
        return time as a datetime object
        """
        try:
            for log_level in ("INFO", "ERROR", "DEBUG"):
                if "[%s]" % log_level in line:
                    s = line.split("[%s]" % log_level)[1].split(",")[0].strip()
            return datetime.datetime.strptime(s, "%Y-%m-%d %H:%M:%S")
        except Exception:
            raise ValueError("Could not get time from %s" % line)

    def _start_end_time_of_a_task_dir(self, task_dir):
        """
        Return start and end time of a task dir/stdout emmitted by pbcommand.
        """
        stdout_fn = op.join(task_dir, "stdout")
        cmd = "cat %s | grep 'Loading pbcommand'| head -1" % stdout_fn
        o, r, m = backticks(cmd)
        start = self._get_time_from_line(o[0])

        cmd = "cat %s | grep 'Completed running'| head -1" % stdout_fn
        o, r, m = backticks(cmd)
        end = self._get_time_from_line(o[0])
        return (start, end)

    def start_end_time_of_task(self, task):
        """Return start and end time of a task.
        Note that a task may be scatter-able, in which case the
        earliest start time of scattered tasks and the latest end time
        of scattered tasks should be returned.
        """
        task_dirs = self.task_dirs(task)
        assert len(task_dirs) > 0
        start, end = self._start_end_time_of_a_task_dir(task_dirs[0])
        for task_dir in task_dirs[1:]:
            s, e = self._start_end_time_of_a_task_dir(task_dir)
            start = start if s > start else s
            end = end if e < end else e
        return (start, end)

    def time_tasks(self, tasks):
        """Get how much time each task has spent and time between neighbouring tasks."""
        starts, ends = [], []
        print "Task\tStartTime\tEndTime\tDurationTime"
        for task in tasks:
            s, e = self.start_end_time_of_task(task)
            starts.append(s)
            ends.append(e)
            # Print start, end and duration time of tasks
            print "\t".join((task, str(s), str(e), str(e-s)))

        # Print time between task[i].start and task[i+1].start
        print "\n"

        print "Task1\tTask2\tTimeBetween"
        for i in range(0, len(tasks)-1):
            print "\t".join((tasks[i], tasks[i+1], str(starts[i+1] - starts[i])))

        return (tasks, starts, ends)

def get_parser():
    """Get parser"""
    description = "Validate smrtlink hgap4 job."
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument("smrtlink_host", type=str, help="SMRTLink HGAP host")
    parser.add_argument("job_id", type=str, help="SMRTLink HGAP job id")
    parser.add_argument("out_dir", type=str, help="Output directory")
    parser.add_argument("--job_dir", "-j", type=str, default=None, help="Override job directory from smrtlink host and job id.")
    return parser


def main(argv=sys.argv[1:]):
    """Main entry"""
    parser = get_parser()
    args = parser.parse_args(argv)

    job_dir = smrtlink_dir(smrtlink_host=args.smrtlink_host, job_id=args.job_id) if args.job_dir is None else args.job_dir
    obj = SMRTLink_HGAP4(root_dir=job_dir)
    #obj.make_links(out_dir=args.out_dir)

    tasks = ['falcon_ns.tasks.task_falcon0_run_merge_consensus_jobs',
             'falcon_ns.tasks.task_falcon0_merge',
             'falcon_ns.tasks.task_falcon0_cons',
             'falcon_ns.tasks.task_falcon1_run_merge_consensus_jobs',
             'falcon_ns.tasks.task_falcon2_run_asm']
    obj.time_tasks(tasks)


if __name__ == "__main__":
    sys.exit(main())
