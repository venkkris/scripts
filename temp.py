from ase.build import molecule
from gpaw import GPAW
from ase.optimize import BFGS

############################
a = 16
xc = 'SCAN'
density = 1e-4
eigenstates = 1e-5
input_str = 'str.cif'
############################

atoms = molecule('F2')
atoms.set_cell((a,a,a))
atoms.center()
calc = GPAW(xc = xc, h=0.16, txt='bfgs.txt', convergence={'density':density,'eigenstates':eigenstates})
atoms.calc = calc
dyn=BFGS(atoms=atoms, trajectory='traj.traj', logfile = 'qn.log', maxstep=0.1)
dyn.run(fmax=0.01)
