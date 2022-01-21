# To plot ab_eos and c_eos when doing bo_nmc or bo_tet
from ase.io import read
from ase.eos import EquationOfState
import matplotlib.pyplot as plt
import glob

ab = glob.glob('ab*.txt')
c = glob.glob('c*.txt')

ea = []
va = []
ec = []
vc = []


for i in ab:
    atoms = read(i)
    ea.append(atoms.get_potential_energy())
    va.append(atoms.get_volume())

for i in c:
    atoms = read(i)
    ec.append(atoms.get_potential_energy())
    vc.append(atoms.get_volume())

# Plot eos_ab
print('Ea: ',ea)
try:
    eos = EquationOfState(va,ea)
    v0, e0, B = eos.fit()
    eos.plot(filename='eos_ab.png')
except:
    print('Plotting eos_ab failed.')
    plt.plot(va,ea,'--*')
    plt.xlabel('Volume')
    plt.ylabel('Energy (eV)')
    plt.savefig('plot_ab.png')
    plt.show()

# Plot eos_c
print('Ec: ',ec)
try:
    eos = EquationOfState(vc,ec)
    v0, e0, B = eos.fit()
    eos.plot(filename='eos_c.png')
except:
    print('Plotting eos_c failed.')
    plt.plot(vc,ec,'--*')
    plt.xlabel('Volume')
    plt.ylabel('Energy (eV)')
    plt.savefig('plot_c.png')
    plt.show()
