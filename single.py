from gpaw import *
from ase.io import read
from ase.parallel import parprint

kpoints = [12,12,6]
gpoints = [16,16,40]

atoms = read('str.cif')
calc = GPAW(xc = 'BEEF-vdW', gpts=gpoints, kpts=kpoints, txt="out.txt")
atoms.set_calculator(calc)
parprint(atoms.get_potential_energy())
atoms.calc.write('out.gpw')
