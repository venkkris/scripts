from gpaw import *
from ase.io import read
from ase.optimize import BFGS


# User inputs
#################################################
kpoints = [12,12,6]
gpoints = [16,16,40]
xc = 'BEEF-vdW'
#################################################

input_structure = "str.cif"
fmaxx = 0.03
maxstep = 0.1


atoms = read(input_structure)
calc = GPAW(xc=xc, gpts=gpoints, kpts=kpoints, txt='bfgs.txt')
atoms.calc = calc
dyn=BFGS(atoms=atoms, trajectory='traj.traj', logfile = 'qn.log', maxstep=maxstep)
dyn.run(fmax=fmaxx)
