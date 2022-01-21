from ase.io import *
import glob
from ase.data import atomic_numbers
import numpy as np
from ase.io.bader import attach_charges


fil = glob.glob('*.gpw')[0]
f = open('ACF.dat','r')


atoms  = read(fil)
sym = atoms.get_chemical_symbols()
Z=[]
for s in sym:
    Z.append(float(atomic_numbers[s]))

n = len(atoms)
vol = []
elec = []
count = 1
for line in f:
    line = line.strip()
    c = line.split()
    if count>2:
        if count<n+3:
            vol.append(float(c[6]))
            elec.append(float(c[4]))
    count = count+1

charge = np.array(Z)-np.array(elec)
sch = []
for i in range(0,len(charge)):
    print (i,sym[i],charge[i])

attach_charges(atoms, 'ACF.dat')
#write('charges.cif',atoms)
