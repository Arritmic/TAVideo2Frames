#!/bin/bash

#1) Create and activate environment
ENVS=$(conda info --envs | awk '{print $1}' )
if [[ $ENVS = *"consa_cv_1"* ]]; then
   source ~/anaconda3/etc/profile.d/conda.sh
   conda activate consa_cv_1
else
   echo "Creating a new conda environment for CV Basic tasks project..."
   conda env create -f environment.yml
   source ~/anaconda3/etc/profile.d/conda.sh
   conda activate consa_cv_1
   #exit
fi;

