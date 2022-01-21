from ase.io import read,write
from ase.visualize import view
from ase import Atom
import os

######### User specified variables #########
atom_index = 8
vacancy_index = 20
str_file = 'str.cif'
############################################

# Get chemical symbols, positions of atom and vacancy site
atoms = read(str_file)
atom_pos = atoms.get_positions()[atom_index]
vacancy_pos = atoms.get_positions()[vacancy_index]
atom_sym = atoms.get_chemical_symbols()[atom_index]

# Create initial and final atoms objects
initial = read(str_file)
del initial[[atom_index,vacancy_index]]
initial.append(Atom(symbol=atom_sym, position=atom_pos))

final = read(str_file)
del final[[atom_index,vacancy_index]]
final.append(Atom(symbol=atom_sym, position=vacancy_pos))

# Create initial and final directories
os.system('mkdir initial')
os.system('mkdir final')

# Write structures to initial/ and final/
write('initial/str.cif',initial)
write('final/str.cif',final)
