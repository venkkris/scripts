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
atoms = read('str.cif')

# Ground state calculation
atoms.calc = GPAW(xc = 'GLLBSC', gpts=gpoints, kpts=kpoints, random=True, occupations=FermiDirac(0.01), txt="gs.txt")
parprint('Potential energy: ', atoms.get_potential_energy())
parprint('Fermi level: ', calc.get_fermi_level())
atoms.calc.write('gs.gpw')




# Band structure calculator
bs_calc = GPAW('gs.gpw').fixed_density(convergence={'bands':'CBM+0.5'}, symmetry='off', kpts={"path": atoms.cell.bandpath().path, 'npoints':100}, txt='bs.txt')
bs = bs_calc.band_structure().subtract_reference()
bs.write('bs.gpw')
bs.plot(filename='band_structure.png', emin=-10, emax=10, show=False)
# parprint('Band gap: ', bandgap(bs_calc))


homo, lumo = bs_calc.get_homo_lumo()
# Calculate the discontinuity potential using the ground state calculator and the accurate HOMO and LUMO
response = calc.hamiltonian.xc.response
dxc_pot = response.calculate_discontinuity_potential(homo, lumo)

# Calculate the discontinuity using the band structure calculator
bs_response = bs_calc.hamiltonian.xc.response
KS_gap, dxc = bs_response.calculate_discontinuity(dxc_pot)

# Fundamental band gap = Kohn-Sham band gap + derivative discontinuity
QP_gap = KS_gap + dxc

print(f'Kohn-Sham band gap:         {KS_gap:.2f} eV')
print(f'Discontinuity from GLLB-sc: {dxc:.2f} eV')
print(f'Fundamental band gap:       {QP_gap:.2f} eV')




# Get DOS and save to dos.csv                                                                        
dos = DOS(bs_calc, npts=500, width=0)
energies = dos.get_energies()
weights = dos.get_dos()
np.savetxt('dos.csv', np.transpose([energies, weights]), delimiter=',', header='energies, weights')

# Plot DOS
plt.close()
ax = plt.gca()
ax.plot(energies, weights)
ax.set_xlabel('Energy [eV]')
ax.set_ylabel('DOS [1/eV]')
plt.savefig('dos.png')
