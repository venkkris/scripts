# Author: Venkatesh Krishnamurthy
# Script to obtain number of cores used by a user
# Usage: running the script without argument returns number of cores used by user with $default_username
# Running the script with argument (that argument being the username of another user) returns the number of cores used by the user with the provided username

default_username=venkatek

username="$1"
if [ -z $username ]
then
    username=$default_username
fi

array=$(squeue -u $username |grep $username |grep R\  |awk '{print $1}')

sum=0
for jobid in $array
do
numcore=$(scontrol show job $jobid |grep NumCPUs |awk '{print $2}' | cut -c 9-)
sum=$(expr $sum + $numcore)
done

echo $username : $sum
