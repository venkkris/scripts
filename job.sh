#!/bin/bash
#
#SBATCH -J b442_Li2
#SBATCH -n 60
#SBATCH -N 1
#SBATCH --time=7-00:00
#SBATCH -A venkvis_gpu
#SBATCH -p gpu
#SBATCH --mem=0
#SBATCH -o job.sh.o%j
#SBATCH --mail-type=ALL
#SBATCH --mail-user=venkatek@andrew.cmu.edu


echo Job started on `hostname` at `date`

spack load py-gpaw
srun --mpi=pmix -n 60 gpaw python relax.py

echo  
echo Job Ended at `date`
