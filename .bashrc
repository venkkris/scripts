# Source global definitions
if [ -f /etc/bashrc ]; then
	. /etc/bashrc
fi


# >>> conda initialize >>>
# !! Contents within this block are managed by 'conda init' !!
__conda_setup="$('/home/venkatek/.miniconda3/bin/conda' 'shell.bash' 'hook' 2> /dev/null)"
if [ $? -eq 0 ]; then
    eval "$__conda_setup"
else
    if [ -f "/home/venkatek/.miniconda3/etc/profile.d/conda.sh" ]; then
        . "/home/venkatek/.miniconda3/etc/profile.d/conda.sh"
    else
        export PATH="/home/venkatek/.miniconda3/bin:$PATH"
    fi
fi
unset __conda_setup
# <<< conda initialize <<<
conda activate vkGPAW_21.6.0


# Spack
source /home/venkatek/spack/share/spack/setup-env.sh

# Changes color of bash prompt to red
export PS1="($CONDA_DEFAULT_ENV)\e[0;34m[Arjuna \W]\$ \e[m"


export PYTHONPATH=/home/venkatek/screening_study/scripts/:$PYTHONPATH
export PYTHONPATH=/home/venkatek/structure_CF/mixture/scripts/:$PYTHONPATH
export PATH=/home/venkatek/software/:$PATH


# User specific aliases and functions
alias q="squeue -u venkatek"
alias cq="clear; q"
alias sq='squeue'
alias sqg='squeue |grep gpu'
alias sqc='squeue |grep cpu'
alias sqh='squeue |grep highmem'
alias sqi='squeue |grep idle'

# Utilities
alias bader_analysis='cp /home/venkatek/scripts/utilities/bader_analysis.sh .; sh bader_analysis.sh; rm bader_analysis.sh '
alias cdp='source /home/venkatek/scripts/utilities/cdp.sh'
alias finalcif='cp ~/scripts/utilities/final_cif_from_traj.py .; py final_cif*.py; rm final_cif*.py'
alias mkjob='sh /home/venkatek/scripts/utilities/mkjob.sh'
alias suggest="cp ~/scripts/utilities/suggest_k_g.py .; py suggest_k_g.py; rm suggest_k_g.py"
alias usage='sh /home/venkatek/scripts/utilities/usage.sh'

# Shorts
alias img="xdg-open"
alias py="python"
alias v="ase gui"
alias c="clear"
alias e="emacs -nw"
alias cls="clear; ls"
alias lsa="ls -la"
alias x="exit"
alias brc="e ~/.bashrc"
alias src="source ~/.bashrc"
alias rmt="rm *~; cls"
alias xc="cat *.py |grep xc\ ="
alias spin="cat *.py |grep spinpol"
alias sub="sbatch job.sh"
alias priority='squeue -o "%.18i %.9P %.10j %.8u %.2t %.10M %.6D %.10Q %.4R"'
alias watchman="watch -n3 squeue -u venkatek"
alias kg='cat *.py |grep kpoints\ ; cat *.py |grep gpoints\ '
alias grid='file="*txt"; cat $file |grep -m 1 --exclude={a*.txt,c*.txt} grid\ s; unset file '
alias vtraj='file="*.traj"; echo "Viewing " $file; v $file &'
alias vfinal="v final.cif &"
alias vstr="v str.cif &"
alias masscancel='for jobid in $(cat job.id); do scancel $jobid; done'


function ndry { gpaw python --dry-run="$1" "$2"; }
export -f ndry


# Need to be tested
alias ch2gpu="sed -i 's/time=7-00:00/time=14-00:00/' job.sh; sed -i 's/venkvis/venkvis_gpu/' job.sh; sed -i 's/-p cpu/-p gpu/' job.sh;"


# Git stuff
#eval "$(ssh-agent -s)"
#ssh-add ~/.ssh/id_ed25519
#export GPG_TTY=$(tty)
