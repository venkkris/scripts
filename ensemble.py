from ase.io import read, write
from gpaw import GPAW
from ase.dft.bee import BEEFEnsemble
from ase.parallel import parprint


#########################################################
kpoints = [12, 12, 5]
gpoints = [16, 16, 36]
xc = 'BEEF-vdW'
#########################################################


atoms = read('final.cif')
calc = GPAW(xc=xc, gpts=gpoints, kpts=kpoints)
atoms.set_calculator(calc)
parprint(atoms.get_potential_energy())

ens = BEEFEnsemble(calc)
ensemble_energies = ens.get_ensemble_energies()

parprint(ensemble_energies)
file = open('ensemble_energies.txt','w')
for energy in ensemble_energies:
    file.write(str(energy)+'\n')
file.close()
