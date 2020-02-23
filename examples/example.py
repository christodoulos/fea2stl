from ucc2stl import dense_cuboids, CuboidComplex

CUBOIDS = dense_cuboids("Node.txt", "Connectivity.txt", "density.txt", 0.3)
CUBOID_COMPLEX = CuboidComplex(CUBOIDS)
CUBOID_COMPLEX.export_off()
CUBOID_COMPLEX.export_stl()
# CUBOID_COMPLEX.export_stl_pymesh()
