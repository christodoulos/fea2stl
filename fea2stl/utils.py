from .primitives import Point

EPSILON = 1.0e-5


def csv2list(afile, atype, prepend_dummy=False):
    "afile is a csv file of atype values, returns a list of tuples"
    print("Opening {} ... ".format(afile), end="")
    alist = []
    for line in open(afile):
        line2list = line.strip().split(",")
        if len(line2list) > 1:
            alist.append(tuple(atype(i) for i in line2list))
        else:
            alist.append(atype(line2list[0]))
    print("Read {} values".format(len(alist)))
    if prepend_dummy:
        alist.insert(0, (0, 0, 0))
    return alist


def dense_cuboids(nodes_file, connectivity_file, density_file, threshold):
    "returns a list of the 'dense' cuboids"
    alist = []
    nodes = csv2list(nodes_file, int, prepend_dummy=True)
    connectivity = csv2list(connectivity_file, int)
    density = csv2list(density_file, float)
    print("Filtering dense cuboids ...", end="")
    for atuple in zip(density, connectivity):
        if atuple[0] - threshold > EPSILON:  # cuboid is 'dense enough'
            cuboid = []
            for vertex in atuple[1]:
                cuboid.append(Point.from_tuple(nodes[vertex]))
            alist.append(cuboid)
    print("Filtered {} dense cuboids".format(len(alist)))
    return alist
