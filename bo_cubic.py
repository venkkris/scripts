# Author: Venkatesh Krishnamurthy

from ase.optimize import BFGS
from gpaw import *
from ase.io import read, write
from ase.parallel import parprint,paropen
from ase.eos import EquationOfState
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

###########################################################################
kpoints = [8,8,8]
gpoints = [24,24,24]
xc = 'PBE'

spin = False          # If true, initialize magnetic moments using magmom
q = 0
#magmom = [0.0]*natoms
density = 1e-4
eigenstates = 4e-8
###########################################################################


step = 0.025
nstep = 5
maxstep = 0.8
fmaxx = 0.03
input_structure = "str.cif"
output_structure = "opt_str.cif"

atoms = read(input_structure)
natoms = len(atoms)
volume = atoms.get_volume()
a=[0]*nstep	# Scaling factor for lattice parameter
e=[0]*nstep	# energy
v=[0]*nstep	# volume


# Optimize lattice parameter
for i in range(nstep):
	a[i] = (1+((nstep//2)-i)*step)**(1./3.)
	atoms = read(input_structure)

	# Scale the cell
	cell = atoms.get_cell()
	cell[:][:] = a[i]*cell[:][:]
	atoms.set_cell(cell,scale_atoms=True)

	# Calculate energy
#	atoms.set_initial_magnetic_moments(magmom)
	calc = GPAW(xc=xc, gpts=gpoints, kpts=kpoints, txt='a'+str(1+((nstep//2)-i)*step)+'.txt', convergence={'density':density,'eigenstates':eigenstates}, charge=q, spinpol=spin)
	atoms.calc = calc
	e[i] = atoms.get_potential_energy()
	v[i] = atoms.get_volume()


# Fit EOS
eos = EquationOfState(v,e)
v0, e0, B = eos.fit()
a_scaling = (v0/volume)**(1./3.)
eos.plot('eos.png', show=False)


# Set atoms to optimized cell parameters and relax atoms
atoms = read(input_structure)
cell = atoms.get_cell()
cell[:][:] = a_scaling*cell[:][:]
atoms.set_cell(cell,scale_atoms=True)
write(output_structure,atoms)

#atoms.set_initial_magnetic_moments(magmom)
calc = GPAW(xc=xc, gpts=gpoints, kpts=kpoints, convergence={'density':density,'eigenstates':eigenstates}, txt='bfgs.txt', charge=q, spinpol=spin)
atoms.calc = calc
dyn=BFGS(atoms=atoms, trajectory='traj.traj', logfile = 'qn.log', maxstep=maxstep)
dyn.run(fmax=fmaxx)
