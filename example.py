"Example usage"

from fea2stl import dense_cuboids, CuboidComplex

# from utils import dense_cuboids
# from cuboids import CuboidComplex

CUBOIDS = dense_cuboids(
    "examples/Node.txt", "examples/Connectivity.txt", "examples/density.txt", 0.3
)
CUBOID_COMPLEX = CuboidComplex(CUBOIDS)
CUBOID_COMPLEX.export_off()
CUBOID_COMPLEX.export_stl()
CUBOID_COMPLEX.export_stl_pymesh()
