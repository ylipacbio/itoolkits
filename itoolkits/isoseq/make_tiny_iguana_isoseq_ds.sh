#!/usr/bin/env bash

# OUTPUT: output directory to put data
outdir=`pwd`/outdir

# INPUT: the full isoseq dataset using the iguana chemistry
full_ds=/pbi/collections/328/3280036/r54006_20170616_211834/1_A01/m54006_170616_212755.subreadset.xml

# INPUT: the existing isoseq job directory of the full dataset
full_ds_isoseq_job_dir=/pbi/dept/secondary/siv/smrtlink/smrtlink-alpha/smrtsuite_170220/userdata/jobs_root/016/016409/tasks/pbtranscript.tasks.combine_cluster_bins-0

# INPUT: GMAP reference genome to compare against
sirv_gmap_ds=/pbi/dept/secondary/siv/testdata/pbtranscript-unittest/data/gmap-referenceset-root-dir/SIRV/gmapreferenceset.xml
#hg38_and_sirv=/pbi/dept/secondary/siv/testdata/isoseq/gmap_db/hg38_and_sirv/hg38_and_sirv/gmapreferenceset.xml

# PARAMETER: number of HQ isoforms cherry-picked from full ds isoseq output
num_hq_isoforms=3
# PARAMETER: number of LQ isoforms cherry-picked from full ds isoseq output
num_lq_isoforms=1

# OUTPUT: where to store the cherry-picked tiny dataset
tiny_ds_data_dir=$outdir/tiny_ds_data
tiny_ds_xml=$tiny_ds_data_dir/$tiny_ds_name.subreadset.xml
# OUTPUT: tiny dataset has a name
tiny_ds_name=tiny_iguana_isoseq
# OUTPUT: running isoseq without genome on the tiny dataset
tiny_ds_isoseq_job_dir=$outdir/tiny_ds_isoseq
tiny_ds_isoseq_w_genome_job_dir=$outdir/tiny_ds_isoseq_w_genome

# Others
this_dir=`pwd`
isoseq_settings_dir=$(dirname `realpath $0`)/isoseq_settings
isoseq_options_xml=$isoseq_settings_dir/isoseq_options.xml
isoseq_w_genome_options_xml=$isoseq_settings_dir/isoseq_w_genome_options.xml
global_options_xml=$isoseq_settings_dir/global_options.xml

function make_tiny_ds()
{
    mkdir -p $tiny_ds_data_dir
    python subset_isoseq_subreads.py $full_ds \
        $full_ds_isoseq_job_dir/cluster_report.csv $full_ds_isoseq_job_dir/hq_isoforms.fasta \
        $full_ds_isoseq_job_dir/lq_isoforms.fasta $tiny_ds_data_dir $tiny_ds_name \
        --num_hq_isoforms=$num_hq_isoforms --num_lq_isoforms=$num_lq_isoforms --random_seed=1
}

# Function run_isoseq_w_genome takes two arguments
# $1 - input subreads dataset
# $2 - output isoseq job directory
# , runs isoseq pipeline on the input subreads dataset
# , and saves results to output isoseq job dir.
function run_isoseq()
{
    # To run isoseq on the tiny dataset and save output to $outdir/run_isoseq_w_genome, do:
    # run_isoseq($tiny_ds_xml $tiny_ds_isoseq_job_dir)
    ds_xml=$1
    job_dir=$2
    echo "Running run_isoseq_w_genome $1 $2"

    job_sh=$job_dir/job.sh
    if [ -f $ds_xml ]; then
        echo 'Found tiny iguana dataset at ' $ds_xml
        mkdir -p $job_dir && cd $job_dir
        echo "pbsmrtpipe pipeline-id pbsmrtpipe.pipelines.sa3_ds_isoseq --debug -e eid_subread:$ds_xml --preset-xml=$isoseq_options_xml --preset-xml=$global_options_xml" | tee $job_sh
        source $job_sh
        cd $this_dir
    else
        echo 'Could not find ' $ds_xml '!'
        echo 'Run example.sh make_tiny_ds first.'
    fi
}

# Function run_isoseq takes three arguments
# $1 - input subreads dataset
# $2 - the GMAP reference dataset
# $3 - output isoseq job directory
# , runs isoseq_w_genome pipeline on the input subreads dataset
# , and saves results to output isoseq job dir.
function run_isoseq_w_genome()
{
    # To run isoseq on the tiny dataset and save output to $outdir/run_isoseq_w_genome, do:
    # run_isoseq($tiny_ds $tiny_ds_isoseq_w_genome_job_dir)
    ds_xml=$1
    gmap_ref_ds=$2
    job_dir=$3
    echo "Running run_isoseq_w_genome $1 $2 $3"

    job_sh=$job_dir/job.sh
    if [ -f $ds_xml ]; then
        echo 'Found tiny iguana dataset at ' $ds_xml
        mkdir -p $job_dir && cd $job_dir
        echo "pbsmrtpipe pipeline-id pbsmrtpipe.pipelines.sa3_ds_isoseq_with_genome --debug -e eid_subread:$ds_xml -e eid_gmapref_dataset:$gmap_ref_ds --preset-xml=$isoseq_options_xml --preset-xml=$global_options_xml" | tee $job_sh
        source $job_sh
        cd $this_dir
    else
        echo 'Could not find ' $ds_xml '!'
        echo 'Run example.sh make_tiny_ds first.'
    fi
}

function usage()
{
    echo "Usage: $0 make_tiny_ds # to make a tiny iguana dataset"
    echo "       $0 run_isoseq   # to run isoseq on the tiny iguana dataset"
    echo "       $0 run_isoseq_w_genome   # to run isoseq within SIRV genome on the tiny iguana dataset"
}

# MAIN

# if no args supplied at the command prompt, display usage message and die
if [ $# -eq 0 ]; then
    usage
else
    if [ $1 == "make_tiny_ds" ]; then
        echo "Making a tiny dataset $tiny_ds_xml by cherry-picking subreads from $full_ds"
        make_tiny_ds
    else
        if [ $1 == "run_isoseq" ]; then 
            echo "Running isoseq pipeline on tiny dataset $tiny_ds_xml, "
            echo "saves to $tiny_ds_isoseq_w_genome_job_dir"
            run_isoseq $tiny_ds_xml $tiny_ds_isoseq_job_dir 
        else
            if [ $1 == "run_isoseq_w_genome" ]; then
                echo "Running isoseq with genome pipeline on tiny dataset $tiny_ds_xml, "
                echo "takes $sirv_gmap_ds as reference and saves to $tiny_ds_isoseq_w_genome_job_dir"
                run_isoseq_w_genome $tiny_ds_xml $sirv_gmap_ds $tiny_ds_isoseq_w_genome_job_dir 
            else
                echo "ERROR: unknown option $1!"
                usage
            fi
        fi
    fi
fi
