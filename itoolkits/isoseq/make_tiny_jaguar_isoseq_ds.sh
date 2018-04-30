set -vex
sr=/pbi/dept/secondary/siv/smrtlink/smrtlink-sms/smrtlink-release_5.1.0.14963/userdata/jobs_root/001/001151/entry-points/06db0526-3c0d-49f1-90e2-7a335178be42.subreadset.xml 
csv=/pbi/dept/secondary/siv/smrtlink/smrtlink-sms/jobs-root/001/001151/tasks/pbtranscript2tools.tasks.create_workspace-0/workspace/cluster_report.FL_nonFL.csv 
hq=/pbi/dept/secondary/siv/smrtlink/smrtlink-sms/jobs-root/001/001151/tasks/pbtranscript2tools.tasks.create_workspace-0/workspace/all_arrowed_hq.100_30_0.99.fasta 
lq=/pbi/dept/secondary/siv/smrtlink/smrtlink-sms/jobs-root/001/001151/tasks/pbtranscript2tools.tasks.create_workspace-0/workspace/all_arrowed_lq.fasta

python subset_isoseq_subreads.py --num_hq_isoforms 10 --num_lq_isoforms 10 $sr $csv $hq $lq  outdir tiny_jaguar
