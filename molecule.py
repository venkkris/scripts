from ase.build import molecule
from gpaw import *
from ase.optimize import BFGS

a = 12
calc = GPAW(xc = 'PBE', h=0.18, txt='bfgs.txt')

atoms = molecule('H2')
atoms.set_cell((a,a,a))
atoms.center()
atoms.calc = calc
dyn=BFGS(atoms=atoms, trajectory='traj.traj', logfile = 'qn.log', maxstep=0.1)
dyn.run(fmax=0.01)
