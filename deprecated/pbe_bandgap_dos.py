from gpaw import GPAW
from ase.io import read
from ase.parallel import parprint
from ase.dft.bandgap import bandgap
from ase.dft.dos import DOS
import numpy as np

kpoints = [12, 12, 5]
gpoints = [16, 16, 40]
xc = 'PBE'

# Do single point DFT calculation
atoms = read('str.cif')
calc = GPAW(xc = xc, gpts=gpoints, kpts=kpoints, txt="out.txt")
atoms.set_calculator(calc)
parprint(atoms.get_potential_energy())

# Alternatively, read from existing gpw file
#atoms = read('out.gpw')


# Compute bandgap
parprint(bandgap(atoms.calc))

# Get dos and save to dos.csv
dos = DOS(atoms.calc, npts=500, width=0)
energies = dos.get_energies()
weights = dos.get_dos()
np.savetxt('dos.csv', np.transpose([energies, weights]), delimiter=',', header='energies, weights')
