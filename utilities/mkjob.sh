#!/bin/bash

# Defaults
default_pyscript=$(ls *.py)
default_partition="gpu"

# If job.sh already exists, move it to old_job.sh
if [ -f job.sh ]; then
    mv job.sh old_job.sh
fi

# Read input from user
read -p "Job name [job_name]: " job_name; job_name=${job_name:-job_name}

read -p "Partition: (cpu/gpu/idle/highmem) [$default_partition]: " partition; partition=${partition:-$default_partition}
if [ $partition == gpu ] ; then
    default_cores=60
elif [[ $partition == cpu || $partition == idle ]] ; then
    default_cores=54
elif [ $partition == highmem ] ; then
    default_cores=30
else
    default_cores=0    
fi

read -p "Number of cores [$default_cores]: " num_cores; num_cores=${num_cores:-$default_cores}
read -p "Number of days [4]: " num_days; num_days=${num_days:-4}
read -p "Python script [$default_pyscript]: " pyscript; pyscript=${pyscript:-$default_pyscript}

# Generate job.sh file
touch job.sh
echo \#!/bin/bash >> job.sh
echo \# >> job.sh
echo \#SBATCH -J $job_name >> job.sh
echo \#SBATCH -n $num_cores >> job.sh
echo \#SBATCH -N 1 >> job.sh
echo \#SBATCH --time=$num_days-00:00 >> job.sh
if [ $partition == gpu ] ; then
    echo \#SBATCH -A venkvis_gpu >> job.sh
else
    echo \#SBATCH -A venkvis >> job.sh
fi
echo \#SBATCH -p $partition >> job.sh

# RAM request
# GPU
if [[ $partition == gpu && $num_cores == 60 ]] ; then
    echo \#SBATCH --mem=0 >> job.sh
elif [[ $partition == gpu && $num_cores -lt 60 ]] ; then
    echo \#SBATCH --mem-per-cpu=2000 >> job.sh
# CPU
elif [[ $partition == cpu && $num_cores == 54 ]] ; then
    echo \#SBATCH --mem=0 >> job.sh
elif [[ $partition == cpu && $num_cores -lt 54 ]] ; then
    echo \#SBATCH --mem-per-cpu=2300 >> job.sh
# Idle
elif [[ $partition == idle && $num_cores == 54 ]] ; then
    echo \#SBATCH --mem=0 >> job.sh
elif [[ $partition == idle && $num_cores -lt 54 ]] ; then
    echo \#SBATCH --mem-per-cpu=2300 >> job.sh
# highmem
elif [[ $partition == highmem && $num_cores == 30 ]] ; then
    echo \#SBATCH --mem=0 >> job.sh
else
    echo \#SBATCH --mem-per-cpu=16000 >> job.sh
fi

echo \#SBATCH -o job.sh.o%j >> job.sh
echo \#SBATCH --mail-type=ALL >> job.sh
echo \#SBATCH --mail-user=venkatek@andrew.cmu.edu >> job.sh
echo >> job.sh
echo >> job.sh
echo echo "Job started on \`hostname\` at \`date\`" >> job.sh
echo >> job.sh
echo spack load py-gpaw >> job.sh
echo srun --mpi=pmix -n $num_cores gpaw python $pyscript >> job.sh
echo >> job.sh
echo echo " " >> job.sh
echo echo "Job Ended at \`date\`" >> job.sh


# Delete variables
unset job_name
unset partition
unset num_cores
unset num_days
unset pyscript
unset default_cores
unset default_pyscript
unset default_partition
