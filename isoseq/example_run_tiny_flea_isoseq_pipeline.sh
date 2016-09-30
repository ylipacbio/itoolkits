# This script runs a tiny flea dataset using the isoseq pipeline

#!/usr/bin/bash

# module load smrtanalysis/mainline

this_dir=`pwd`
out_dir=$this_dir/outdir
tiny_xml=$out_dir/tiny_flea_isoseq.subreads.xml
setting_dir=$this_dir/isoseq_settings

if [ -f $tiny_xml ]; then
    echo 'Found tiny flea dataset at ' $tiny_xml
    cp $setting_dir/* $out_dir/
    cd $out_dir
    echo pbsmrtpipe pipeline-id pbsmrtpipe.pipelines.sa3_ds_isoseq --debug -e eid_subread:$tiny_xml --preset-xml=$out_dir/isoseq_options.xml --preset-xml=$out_dir/global_options.xml
    cd $this_dir
else
    echo 'Could not find ' $out_dir ' or ' $tiny_xml '!'
    echo 'Run example_make_tiny_flea_isoseq_data.sh first.'
fi



