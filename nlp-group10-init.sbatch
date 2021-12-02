#!/bin/bash
#SBATCH --nodes=3                        # requests 3 compute servers
#SBATCH --ntasks-per-node=2              # runs 2 tasks on each server
#SBATCH --cpus-per-task=2                # uses 1 compute core per task
#SBATCH --time=1:00:00
#SBATCH --mem=4000
#SBATCH --job-name=nlp-group10-init
#SBATCH --output=nlp-group10-init.out

module purge; 
source env/bin/activate;
export OMP_NUM_THREADS=$SLURM_CPUS_PER_TASK;
python main.py