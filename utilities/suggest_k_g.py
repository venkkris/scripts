from ase.io import read
from gpaw.utilities import h2gpts
import glob
import os

##########################
product = 30
h = 0.16
##########################

#print()
try:
    atoms = read('str.cif')
except:
    filenames = glob.glob('*.cif')
    atoms = read(filenames[0])
    print('Read '+filenames[0]+'\n')

#cellpar = atoms.get_cell_lengths_and_angles()
cellpar = atoms.cell.cellpar()
a = cellpar[0]
b = cellpar[1]
c = cellpar[2]
#print('a: ',a)
#print('b: ',b)
#print('c: ',c)
#print()

kx = int(product//a+1)
ky = int(product//b+1)
kz = int(product//c+1)
kpoints = [kx,ky,kz]
print('Suggested k-points: ',kpoints)
print()
print('Products: ',[kx*a,ky*b,kz*c])
print('\n')


h = input("Specify h: ")
h = float(h)
tmp = h2gpts(h,atoms.get_cell(),idiv=8)
gpoints = [tmp[0],tmp[1],tmp[2]]
print('\nSuggested g-points: ',gpoints)
print()
print('h: ',[a/gpoints[0],b/gpoints[1],c/gpoints[2]])
print()

response = input('Edit *.py? (yes/no): ')
if response=='yes':
    # Change the k and gpoints in *.py
    newkpts = "kpoints = "+str(kpoints)
    command = "sed -i 's/^kpoints\ =\ .*/"+newkpts+"/' *.py"
    os.system(command)
    newgpts = "gpoints = "+str(gpoints)
    command = "sed -i 's/^gpoints\ =\ .*/"+newgpts+"/' *.py"
    os.system(command)
    print('Edited kpoints and gpoints line in *.py')
else:
    print('*.py not edited.')
