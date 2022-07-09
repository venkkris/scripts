from gpaw import *
from ase.io import read
from ase.parallel import parprint

kpoints = [12, 12, 6]
gpoints = [16, 16, 40]
xc = 'PBE'

atoms = read('final.cif')
calc = GPAW(xc = xc, gpts=gpoints, kpts=kpoints, txt="out.txt")
atoms.calc = calc
parprint(atoms.get_potential_energy())
atoms.calc.write('out.gpw')
