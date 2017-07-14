My toolkits for internal analysis. 

Directory **isoseq/** contains scripts for testing the Iso-Seq pipeline.

+ **subset_isoseq_subreads.py**
    a python script which subsets input bam by cherry-picking subreads which support a few HQ/LQ isoforms based on existing Iso-Seq analysis of the input bam.
    
+ **example.sh**
    To use subset_isoseq_subreads.py to make a tiny dataset and how to run isoseq on the tiny dataset.
   ```
       ./example.sh make_tiny_ds # to make a tiny flea dataset
       ./example.sh run_isoseq   # to run isoseq on the tiny flea dataset
       ./example.sh run_isoseq_w_genome   # to run isoseq within SIRV genome on the tiny flea dataset
   ```

+ **make_tiny_iguana_isoseq_ds**
    To make a tiny subset of data from an Iguana RC0 SMRTCell:
    ```
        ./make_tiny_iguana_isoseq_ds.sh make_tiny_ds
        ./make_tiny_iguana_isoseq_ds.sh run_isoseq_w_genome
    ```

+ **make_medium_iguana_isoseq_ds**
    To make a medium-size subset of data from an Iguana RC0 SMRTCell:
    ```
        ./make_medium_iguana_isoseq_ds.sh make_ds
        ./make_medium_iguana_isoseq_ds.sh run_isoseq_w_genome
    ```
   
   
