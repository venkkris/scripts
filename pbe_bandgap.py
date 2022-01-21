from gpaw import *
from ase.io import read
from ase.parallel import parprint
from ase.dft.bandgap import bandgap
from ase.dft.dos import DOS
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt


kpoints = [12, 12, 6]
gpoints = [20, 20, 48]
spinpol = False # Whether calculation is spin-polarized or not

atoms = read('str.cif')
#magmoms = [0.0]*len(atoms)
#atoms.set_initial_magnetic_moments(magmoms)


# Ground state calculation
calc = GPAW(xc = 'PBE', gpts=gpoints, kpts=kpoints, spinpol=spinpol, random=True, txt="gs.txt")
atoms.set_calculator(calc)
parprint('Potential energy: ', atoms.get_potential_energy())
parprint('Fermi level: ', calc.get_fermi_level())
#if spinpol==False:
#    parprint('Default band gap: ',bandgap(atoms.calc))
#else:
#    parprint('Default band gap, spin up: ', bandgap(atoms.calc, spin=0))
#    parprint('Default band gap, spin down: ', bandgap(atoms.calc, spin=1))
atoms.calc.write('gs.gpw')


# Save plot of BZ
lat = atoms.cell.get_bravais_lattice()
fig = lat.plot_bz(show=False).get_figure()
fig.savefig('bz.png', bbox_inches='tight')
fig.clear()




# Band structure calculator
bs_calc = GPAW('gs.gpw').fixed_density(convergence={'bands':'CBM+0.5'}, symmetry='off', kpts={"path": atoms.cell.bandpath().path, 'npoints':100}, txt='bs.txt')
bs = bs_calc.band_structure().subtract_reference()
bs.write('bs.gpw')
bs.plot(filename='band_structure.png', emin=-10, emax=10, show=False)

if spinpol==False:
    parprint('New band gap: ', bandgap(bs_calc))
else:
    parprint('New band gap, spin up: ', bandgap(bs_calc, spin=0))
    parprint('New band gap, spin down: ', bandgap(bs_calc, spin=1))




# Get dos and save to dos.csv                                                                        
dos = DOS(calc, npts=500, width=0)
energies = dos.get_energies()
weights = dos.get_dos()
np.savetxt('dos.csv', np.transpose([energies, weights]), delimiter=',', header='energies, weights')

plt.close()
ax = plt.gca()
ax.plot(energies, weights)
ax.set_xlabel('Energy [eV]')
ax.set_ylabel('DOS [1/eV]')
plt.savefig('dos.png')
