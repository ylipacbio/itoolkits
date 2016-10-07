My toolkits for internal analysis. 

Directory **isoseq/** contains scripts for testing the Iso-Seq pipeline.

+ **subset_isoseq_subreads.py**
    a python script which subsets input bam by cherry-picking subreads which support a few HQ/LQ isoforms based on existing Iso-Seq analysis of the input bam.
    
+ **example.sh**
   ```
      ./example.sh make_tiny_ds # to make a tiny flea dataset
      ./example.sh run_isoseq   # to run isoseq on the tiny flea dataset
      ./example.sh run_isoseq_w_genome   # to run isoseq within SIRV genome on the tiny flea dataset
   ```

   
   
