#!/bin/bash                                                                                      
#                                                                                                
#SBATCH -J job_name
#SBATCH -n 54
#SBATCH -N 1
#SBATCH --time=7-00:00
#SBATCH -A venkvis
#SBATCH -p cpu
#SBATCH --mem=0
#SBATCH -o job.sh.o%j
#SBATCH --mail-type=ALL
#SBATCH --mail-user=venkatek@andrew.cmu.edu


echo "Job started on `hostname` at `date`"

spack load py-gpaw
srun -n 54 gpaw python relax_magnetic.py

echo " "
echo "Job Ended at `date`"
