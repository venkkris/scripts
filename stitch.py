from ase.io.trajectory import TrajectoryWriter, Trajectory

traj1 = Trajectory('killed/traj.traj')
traj2 = Trajectory('traj.traj')
writer = TrajectoryWriter('combined.traj', 'w')
for atoms in traj1:
    writer.write(atoms)
for atoms in traj2:
    writer.write(atoms)
writer.close()
