from ase.neb import NEBTools
from ase.io import read,write
import glob
import matplotlib.pyplot as plt


trajname = glob.glob('initial/*.traj')
a1 = read(trajname[0])
a2 = read('2.txt')
a3 = read('3.txt')
a4 = read('4.txt')
trajname = glob.glob('final/*.traj')
a5 = read(trajname[0])

e = []
images = []
x = [0,1,2,3,4]
e.append(a1.get_potential_energy())
e.append(a2.get_potential_energy())
e.append(a3.get_potential_energy())
e.append(a4.get_potential_energy())
e.append(a5.get_potential_energy())
images.append(a1)
images.append(a2)
images.append(a3)
images.append(a4)
images.append(a5)


# Plot temporary energy vs stage plot
min_e = min(e)
for i in range(len(e)):
    e[i] -= min_e
plt.plot(x,e,'-*')
plt.savefig('temp.png')
plt.close()


# Write energies to file
file = open('energies.txt','w')
for energy in e:
    file.write(str(energy)+'\n')
file.close()


# Write traj file
write('delete.traj',images)


# Try to plot barrier
nebtools = NEBTools(images)
Ef, dE = nebtools.get_barrier()
fig = nebtools.plot_band()
fig.savefig('diffusion-barrier.png')
