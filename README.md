# Pathogen-Pipeline

Dependencies:
Nextflow 21.* (Requires Java 8-15 && Bash 3.2 or higher) https://www.nextflow.io/docs/latest/getstarted.html
Singularity 3.8.* (Requires Linux System and other dependencies listed on https://sylabs.io/guides/3.0/user-guide/quick_start.html)

Instructions for execution:
1. Build singularity image file: 'sudo singularity build pipeline.sif pipeline.def'
2. Upon successful singularity build execute nextflow: 'nextflow run main.nf -with-singularity pipeline.sif --model (xgb/keras)' choosing either xgb or keras to train
3. Partially completed workflow can be resumed by using the -resume flag when running nextflow 
