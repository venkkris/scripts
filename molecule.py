from ase.build import molecule
from gpaw import *
from ase.optimize import BFGS

a = 10
calc = GPAW(xc='BEEF-vdW', h=0.20, txt='bfgs.txt')

system = molecule('H2')
system.set_cell((a,a,a))
system.center()
system.calc = calc
dyn=BFGS(atoms=system, trajectory='traj.traj', logfile = 'qn.log', maxstep=0.1)
dyn.run(fmax=0.01)
