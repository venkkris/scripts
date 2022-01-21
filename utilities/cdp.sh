cd $(scontrol show job "$1" |awk '/WorkDir/' |xargs |cut -c 9-)
