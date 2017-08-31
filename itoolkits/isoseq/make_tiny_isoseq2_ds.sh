# Make a tiny isoseq ds for testing isoseq2, which contains 
# * one HQ human isoform
# * one HQ SIRV isoform
# * one random LQ isoform
#i0_HQ_sample1845e4|c15999/f4p0/462 SIRV109
#i1_HQ_sample1845e4|c34319/f2p33/1402 EEF1G-001|EEF1G -6990 99.9286 0 3 1402 1402 0 113 1513 1523 254
# The input subreads come from Iguana v5.0

sr=/pbi/collections/328/3280036/r54006_20170616_211834/1_A01/m54006_170616_212755.subreadset.xml 
csv=/pbi/dept/secondary/siv/smrtlink/smrtlink-nightly/smrtsuite_5.0.1.9585/userdata/jobs_root/000/000595/tasks/pbtranscript.tasks.separate_flnc-0/combined/all.cluster_report.csv 
hq=/pbi/dept/secondary/siv/smrtlink/smrtlink-nightly/smrtsuite_5.0.1.9585/userdata/jobs_root/000/000595/tasks/pbtranscript.tasks.separate_flnc-0/combined/all.polished_hq.fasta 
lq=/pbi/dept/secondary/siv/smrtlink/smrtlink-nightly/smrtsuite_5.0.1.9585/userdata/jobs_root/000/000595/tasks/pbtranscript.tasks.separate_flnc-0/combined/all.polished_lq.fasta

subset_isoseq_subreads.py $sr $csv $hq $lq outdir tiny_isoseq2_ds --hq_cluster_ids 'i0_ICE_sample1845e4|c15999;i1_ICE_sample1845e4|c34319'
