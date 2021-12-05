#!/bin/bash
#SBATCH --nodes=1                        # requests 3 compute servers
#SBATCH --ntasks-per-node=1              # runs 2 tasks on each server
#SBATCH --cpus-per-task=1                # uses 1 compute core per task
#SBATCH --time=2:00:00
#SBATCH --mem=4000
#SBATCH --job-name=nlp-group10-init
#SBATCH --output=nlp-group10-init.out

module purge; 
source env/bin/activate;
export OMP_NUM_THREADS=$SLURM_CPUS_PER_TASK;
python determination-test.py