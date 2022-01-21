import glob
import numpy as np
from ase.eos import EquationOfState
from ase.io import read
import matplotlib.pyplot as plt

e = []
v = []
list = glob.glob('a*.txt')
for file in list:
    atoms = read(file)
    e.append(atoms.get_potential_energy())
    v.append(atoms.get_volume())

try:
    eos = EquationOfState(v,e)
    v0, e0, B = eos.fit()
    eos.plot('eos.png',show=None)
except:
    print('Plotting failed.')
    plt.plot(v,e,'--*')
    plt.xlabel('Volume')
    plt.ylabel('Energy (eV)')
    plt.savefig('eos.png')
