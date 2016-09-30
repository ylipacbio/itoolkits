# This script makes a tiny isoseq dataset using flea chemistry.

#!/usr/bin/bash

# module load smrtanalysis/mainline

d=/pbi/dept/secondary/siv/smrtlink/smrtlink-alpha/smrtsuite_170220/userdata/jobs_root/000/000626/tasks/pbtranscript.tasks.combine_cluster_bins-0

python subset_isoseq_subreads.py \
/pbi/collections/315/3150353/r54086_20160831_010819/4_D01/m54086_160831_230338.subreads.bam \
$d/cluster_report.csv $d/hq_isoforms.fasta $d/lq_isoforms.fasta outdir outprefix \
--num_hq_isoforms=3 --num_lq_isoforms=2 --random_seed=1
