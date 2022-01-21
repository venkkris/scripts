from ase.io import read
from gpaw import *
from ase.parallel import parprint

######################### Key settings
kpoints = [12, 12, 5]
gpoints = [16, 16, 40]
xc = 'GLLBSC'
#########################


# Single point DFT calculation
atoms = read('str.cif')
calc = GPAW(xc=xc, gpts=gpoints, kpts=kpoints, txt="out.txt", occupations=FermiDirac(0.01))
atoms.set_calculator(calc)
atoms.get_potential_energy()
atoms.calc.write('out.gpw')


# Band structure calculation with fixed density
bs_calc = calc.fixed_density(nbands=22,
                             kpts={'path': 'GAHKLM', 'npoints': 60},
                             symmetry='off',
                             convergence={'bands': 20},
                             txt='bs.out')

# Plot the band structure
#bs = bs_calc.band_structure().subtract_reference()
#bs.plot(filename='bs_si.png', emin=-6, emax=6)


homo, lumo = calc.get_homo_lumo()
response = calc.hamiltonian.xc.response
dxc_pot = response.calculate_discontinuity_potential(homo, lumo)
KS_gap, dxc = response.calculate_discontinuity(dxc_pot)

# Fundamental band gap = Kohn-Sham band gap + derivative discontinuity
QP_gap = KS_gap + dxc

parprint(f'Kohn-Sham band gap:         {KS_gap:.2f} eV')
parprint(f'Discontinuity from GLLB-sc: {dxc:.2f} eV')
parprint(f'Fundamental band gap:       {QP_gap:.2f} eV')
