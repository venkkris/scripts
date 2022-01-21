from gpaw import *
from ase.io import read, write
from ase.eos import EquationOfState
from ase.optimize import BFGS
import numpy as np
import math as m


# User inputs
#################################################################
kpoints = [4, 4, 2]
gpoints = [48, 48, 96]
xc = 'BEEF-vdW'
spin = True    # Initialize magnetic moments
niter = 3

ele1 = 'Co'
magmom1 = 0.0
ele2 = 'Mn'
magmom2 = 3.0
ele3 = 'Ni'
magmom3 = 2.0
#################################################################

input_structure = "str.cif"
output_structure = "opt_str.cif"
step = 0.025
nstep = 5
maxstep = 0.1
fmaxx = 0.03


# Other variables
atoms = read(input_structure)
volume = atoms.get_volume()
magmom = [0.0]*len(atoms)
sym = atoms.get_chemical_symbols()
a=[0]*nstep	# Scaling factor for lattice parameter a
b=[0]*nstep	# Scaling factor for lattice parameter b
c=[0]*nstep	# Scaling factor for lattice parameter c
e=[0]*nstep	# energy
v=[0]*nstep	# volume

# Initialize magnetic moments
for i in range(len(magmom)):
        if sym[i]==ele1:
                magmom[i]=magmom1
        if sym[i]==ele2:
                magmom[i]=magmom2
        if sym[i]==ele3:
                magmom[i]=magmom3


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
	atoms.set_initial_magnetic_moments(magmom)
	calc = GPAW(xc=xc,eigensolver=Davidson(niter),spinpol=spin, gpts=gpoints, kpts=kpoints, txt='ab'+str(1+((nstep//2)-i)*step)+'.txt', mixer=MixerSum(0.05, 2, 100))
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
        atoms.set_initial_magnetic_moments(magmom)
        calc = GPAW(xc=xc, eigensolver=Davidson(niter), spinpol=spin, gpts=gpoints, kpts=kpoints, txt='c'+str(c[i])+'.txt', mixer=MixerSum(0.05, 2, 100))
        atoms.set_calculator(calc)
        e[i] = atoms.get_potential_energy()
        v[i] = atoms.get_volume()


# Fit EOS
eos_c = EquationOfState(v,e,eos='birchmurnaghan')
v0, e0, B = eos_c.fit()
c_scaling = v0/(volume*ab_scaling*ab_scaling)


# Set atoms to optimized cell parameters
atoms = read(input_structure)
calc = GPAW(xc=xc, eigensolver=Davidson(niter), spinpol=spin, gpts=gpoints, kpts=kpoints, mixer=MixerSum(0.05, 2, 100))
atoms.set_calculator(calc)
cell = atoms.get_cell()
cell[0][:] = ab_scaling*cell[0][:]
cell[1][:] = ab_scaling*cell[1][:]
cell[2][:] = c_scaling*cell[2][:]
atoms.set_cell(cell,scale_atoms=True)
atoms.set_initial_magnetic_moments(magmom)

# Do atom relax and write outputs
write(output_structure,atoms)
atoms.calc.set(txt='relax.txt')
dyn=BFGS(atoms=atoms, trajectory='traj.traj', logfile = 'qn.log', maxstep=maxstep)
dyn.run(fmax=fmaxx)
