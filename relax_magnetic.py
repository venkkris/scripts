from gpaw import *
from ase.io import read
from ase.optimize import BFGS


# User inputs
#####################################################
kpoints = [12,12,6]
gpoints = [16,16,40]
xc = 'BEEF-vdW'
#####################################################

input_structure = "str.cif"
atoms = read(input_structure)
fmaxx = 0.03
maxstep = 0.1

# Spin settings
niter = 3
spin = True
ele1 = 'Ni'
magmom1 = 2.0
ele2 = 'Mn'
magmom2 = 3.0
ele3 = 'Co'
magmom3 = 0.0

natoms = len(atoms)
magmom = [0.0]*natoms
sym = atoms.get_chemical_symbols()

# Initialize magnetic moments
for i in range(len(magmom)):
        if sym[i]==ele1:
                magmom[i]=magmom1
        if sym[i]==ele2:
                magmom[i]=magmom2
        if sym[i]==ele3:
                magmom[i]=magmom3
atoms.set_initial_magnetic_moments(magmoms=magmom)


calc = GPAW(xc=xc, gpts=gpoints, kpts=kpoints, spinpol=spin, mixer=MixerSum(0.05, 2, 100), eigensolver=Davidson(niter), txt='bfgs.txt')
atoms.calc = calc
dyn=BFGS(atoms=atoms, trajectory='traj.traj', logfile = 'qn.log', maxstep=maxstep)
dyn.run(fmax=fmaxx)
