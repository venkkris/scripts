from ase.io import write
from ase.io.trajectory import Trajectory
import glob

filename = glob.glob('*.traj')

atoms = Trajectory(filename[-1])[-1]
write('final.cif',atoms)
print('Wrote final structure of ',filename[-1])
