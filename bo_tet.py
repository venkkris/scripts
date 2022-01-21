from ase.optimize import BFGS
from gpaw import *
from ase.io import read, write
from ase.eos import EquationOfState
import numpy as np
import math as m


# User inputs
############################################################
kpoints = [12, 12, 6]
gpoints = [48, 48, 96]
xc = 'BEEF-vdW'
############################################################


step = 0.025
nstep = 5
maxstep = 0.1
fmaxx = 0.03

input_structure = "str.cif"
output_structure = "opt_str.cif"

# Other variables
atoms = read(input_structure)
volume = atoms.get_volume()
natoms = len(atoms)
a=[0]*nstep	# Scaling factor for lattice parameter a
b=[0]*nstep	# Scaling factor for lattice parameter b
c=[0]*nstep	# Scaling factor for lattice parameter c
e=[0]*nstep	# energy
v=[0]*nstep	# volume


# Optimize a and b simultaneuously
for i in range(nstep):
	a[i] = m.sqrt(1+((nstep//2)-i)*step)
	b[i] = m.sqrt(1+((nstep//2)-i)*step)
	c[i] = 1
	atoms = read(input_structure)

	# Scale the cell
	cell = atoms.get_cell()
	cell[0][:] = a[i]*cell[0][:]
	cell[1][:] = b[i]*cell[1][:]
	cell[2][:] = c[i]*cell[2][:]
	atoms.set_cell(cell,scale_atoms=True)

        # Calculate energy
	calc = GPAW(xc=xc, gpts=gpoints, kpts=kpoints, txt='ab'+str(1+((nstep//2)-i)*step)+'.txt')
	atoms.set_calculator(calc)
	e[i] = atoms.get_potential_energy()
	v[i] = atoms.get_volume()


# Fit EOS
eos_a = EquationOfState(v,e,eos='birchmurnaghan')
v0, e0, B = eos_a.fit()
ab_scaling = m.sqrt(v0/volume)


# Optimize c
for i in range(nstep):
        a[i] = ab_scaling
        b[i] = ab_scaling
        c[i] = 1 + ((nstep//2)-i)*step
        atoms = read(input_structure)

	# Scale the cell along c
        cell = atoms.get_cell()
        cell[0][:] = a[i]*cell[0][:]
        cell[1][:] = b[i]*cell[1][:]
        cell[2][:] = c[i]*cell[2][:]
        atoms.set_cell(cell,scale_atoms=True)

	# Calculate energy
        calc = GPAW(xc=xc, gpts=gpoints, kpts=kpoints, txt='c'+str(c[i])+'.txt')
        atoms.set_calculator(calc)
        e[i] = atoms.get_potential_energy()
        v[i] = atoms.get_volume()


# Fit EOS
eos_c = EquationOfState(v,e,eos='birchmurnaghan')
v0, e0, B = eos_c.fit()
c_scaling = v0/(volume*ab_scaling*ab_scaling)


# Set atoms to optimized cell parameters
atoms = read(input_structure)
calc = GPAW(xc=xc, gpts=gpoints, kpts=kpoints)
atoms.set_calculator(calc)
cell = atoms.get_cell()
cell[0][:] = ab_scaling*cell[0][:]
cell[1][:] = ab_scaling*cell[1][:]
cell[2][:] = c_scaling*cell[2][:]
atoms.set_cell(cell,scale_atoms=True)

# Do atom relax and write outputs
write(output_structure,atoms)
atoms.calc.set(txt='relax.txt')
dyn=BFGS(atoms=atoms, trajectory='traj.traj', logfile = 'qn.log', maxstep=maxstep)
dyn.run(fmax=fmaxx)
