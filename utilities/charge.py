from gpaw import *
from ase.io import read, write
from ase.units import Bohr,Rydberg,kJ,kB
import glob


fil = glob.glob('*.gpw')[0]

# Create density.cube file
atoms = read(fil)
calc = GPAW(fil)
density = calc.get_all_electron_density() * Bohr**3
write('density.cube', atoms, data=density)
