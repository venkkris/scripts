from gpaw import *
from ase.io import read
from ase.parallel import parprint
from ase.dft.bandgap import bandgap
import matplotlib
matplotlib.use('Agg')


kpoints = [7, 7, 7]
gpoints = [48, 48, 80]
spin = False

atoms = read('str.cif')
#magmoms = [0.0]*len(atoms)
#atoms.set_initial_magnetic_moments(magmoms)


calc = GPAW(xc = 'PBE', gpts=gpoints, kpts=kpoints, spinpol=spin, random=True, txt="out.txt")
atoms.set_calculator(calc)
parprint(atoms.get_potential_energy())
Ef = calc.get_fermi_level()
atoms.calc.write('out.gpw')
parprint('Fermi level: ', Ef)
parprint('Default: ',bandgap(atoms.calc))


# Band structure calculator
parprint('Starting band structure calculation...')
bs_calc = GPAW('out.gpw').fixed_density(
    nbands = 16,
    symmetry='off',
    kpts={"path": atoms.cell.bandpath().path},
    txt='bs.txt')

bs = bs_calc.band_structure().subtract_reference()
parprint('Plotting band structure...')
bs.plot(filename='band_structure.png', emin=-6, emax=6, show=False)
parprint('New bandgap: ', bandgap(atoms.bc_calc))
