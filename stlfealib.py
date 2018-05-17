"""
stlfealib is a python3 library that calculates the outer shell of a unit cube
complex
"""

EPSILON = 1.0E-5


def csv2list(afile, atype, prepend_dummy=False):
    "afile is a csv file of atype values, returns a list of tuples"
    print("Opening {} ... ".format(afile), end='')
    alist = []
    for line in open(afile):
        line2list = line.strip().split(',')
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
    print("Filtering dense cuboids ...", end='')
    for atuple in zip(density, connectivity):
        if atuple[0] - threshold > EPSILON:  # cuboid is 'dense enough'
            cuboid = []
            for vertex in atuple[1]:
                cuboid.append(Point.from_tuple(nodes[vertex]))
            alist.append(cuboid)
    print("Filtered {} dense cuboids".format(len(alist)))
    return alist


class Point(object):
    "A class for 3D points"

    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    @classmethod
    def from_point(cls, point):
        "Initializes a 3D point from another point"
        return cls(point.x, point.y, point.z)

    @classmethod
    def from_tuple(cls, tup):
        "Initializes a 3D point from a tuple of 3 values"
        return cls(tup[0], tup[1], tup[2])

    @property
    def coordinates(self):
        "Returns the coordinates of the 3D point"
        return self.x, self.y, self.z

    def __repr__(self):
        return 'Point({0},{1},{2})'.format(self.x, self.y, self.z)

    def __hash__(self):
        return hash((self.x, self.y, self.z))

    def __eq__(self, other):
        if not other:
            return False
        return (self.x, self.y, self.z) == (other.x, other.y, other.z)

    def __ne__(self, other):
        if not other:
            return True
        return (self.x, self.y, self.z) != (other.x, other.y, other.z)

    def __lt__(self, other):
        return (self.x, self.y, self.z) < (other.x, other.y, other.z)

    def __gt__(self, other):
        return (self.x, self.y, self.z) > (other.x, other.y, other.z)

    def __le__(self, other):
        return (self.x, self.y, self.z) <= (other.x, other.y, other.z)

    def __ge__(self, other):
        return (self.x, self.y, self.z) >= (other.x, other.y, other.z)

    def __getitem__(self, index):
        return (self.x, self.y, self.z)[index]

    def __setitem__(self, index, value):
        temp = [self.x, self.y, self.z]
        temp[index] = value
        self.x, self.y, self.z = temp

    def __iter__(self):
        yield self.x
        yield self.y
        yield self.z

    def __sub__(self, other):
        "Subtracts two points giving the vector that translates other to self"
        return Vector(other.x - self.x, other.y - self.y, other.z - self.z)

    def __add__(self, vector):
        "Translates self to another points using 'vector' vector"
        return Point(self.x + vector.x, self.y + vector.y, self.z + vector.z)


class Vector(Point):

    "docstring"

    def __init__(self, *args):
        if not args:
            x, y, z = 0, 0, 0
        elif len(args) == 1:
            if args[0].__class__ is Point:
                x, y, z = args[0].x, args[0].y, args[0].z
            else:
                x, y, z = args[0], 0, 0
        elif len(args) == 2:
            x, y, z = args[0], args[1], 0
        else:
            x, y, z = args[0], args[1], args[2]
        self.coords = [x, y, z]
        super(Vector, self).__init__(x, y, z)

    def __repr__(self):
        return "Vector({1}{0}{2}{0}{3})".format(',', self.x, self.y, self.z)

    @property
    def magnitude2(self):
        "Returns the squared magnitude of the vector."
        return self.x**2 + self.y**2 + self.z**2

    def cross(self, vector):
        "Returns the cross product of self and vector"
        return Vector(
            (self.y * vector.z - self.z * vector.y),
            (self.z * vector.x - self.x * vector.z),
            (self.x * vector.y - self.y * vector.x))


class Segment(object):

    "docstring"

    def __init__(self, start, end):
        self.start = start
        self.end = end

    @classmethod
    def from_segment(cls, segment):
        "docstring"
        return cls(segment.start, segment.end)

    def __repr__(self):
        return "Segment(%s, %s)" % (self.start, self.end)

    def __eq__(self, other):
        return self.start == other.start and self.end == other.end


class Face(object):

    "docstring"

    def __init__(self, vertices):
        "self.vertices is an iterable of Point"
        self.vertices = vertices

    def __repr__(self):
        _repr = '\nFace\n'
        for vertex in self.vertices:
            _repr += '\t%s\n' % vertex
        return _repr

    def normal(self):
        "docstring"
        v = self.vertices
        v1 = v[0] - v[1]
        v2 = v[0] - v[2]
        return v1.cross(v2)


class Cuboid(object):

    "docstring"

    def __init__(self, vertices):
        self.vertices = sorted(vertices)
        v = self.vertices
        self.facedict = {
            'north': Face([v[0], v[2], v[6], v[4]]),
            'south': Face([v[1], v[5], v[7], v[3]]),
            'east': Face([v[5], v[4], v[6], v[7]]),
            'west': Face([v[0], v[1], v[3], v[2]]),
            'top': Face([v[6], v[2], v[3], v[7]]),
            'bottom': Face([v[0], v[4], v[5], v[1]])
        }

    def __repr__(self):
        _repr = '\nCuboid:\n--------\nVertices\n--------\n'
        for vertex in self.vertices:
            _repr += '\t%s\n' % vertex
        _repr += '-----\nFaces\n-----\n'
        for orientation, face in self.faces:
            _repr += '{0}: {1}'.format(orientation, face)
        return _repr

    def __eq__(self, other):
        return self.centroid == other.centroid

    def __ne__(self, other):
        return self.centroid != other.centroid

    def __lt__(self, other):
        return self.centroid < other.centroid

    def __qt__(self, other):
        return self.centroid > other.centroid

    def __le__(self, other):
        return self.centroid <= other.centroid

    def __ge__(self, other):
        return self.centroid >= other.centroid

    @property
    def faces(self):
        "docstring"
        for orientation, face in self.facedict.items():
            yield orientation, face

    @property
    def centroid(self):
        "Returns the centroid of the cuboid"
        x, y, z = 0.0, 0.0, 0.0
        for vertex in self.vertices:
            x += vertex.x
            y += vertex.y
            z += vertex.z
        return Point(x / 8.0, y / 8.0, z / 8.0)


class CuboidComplex(object):

    "A class that handles unit cube complexes in 3D space"

    def __init__(self, cuboids):
        self.cubdict = dict()
        self.shell_triangles = list()
        self.shell_vertices = list()
        print("Started inserting cuboids ... ", end='')
        for cuboid in cuboids:
            self.insert(Cuboid(cuboid))
        print("Done inserting {} cuboids".format(len(cuboids)))

    def shell(self):
        "docstring"
        print('Started outer shell calculation  ... ', end='')
        vdict = dict()
        nvs = -1
        for cuboid, faces_info in self.cubdict.items():
            for face_label, face_info in faces_info.items():
                if face_info['out']:
                    tface = []
                    for vertex in face_info['face'].vertices:
                        coords = (vertex.x, vertex.y, vertex.z)
                        if coords not in vdict:
                            nvs += 1
                            self.shell_vertices.append(coords)
                            vdict[coords] = nvs
                        tface.append(vdict[coords])
                    tri1 = [tface[0], tface[1], tface[2]]
                    tri2 = [tface[2], tface[3], tface[0]]
                    self.shell_triangles += [tri1, tri2]
        print('Done\nThere are {} vertices and {} triangles'.format(len(
            self.shell_vertices), len(self.shell_triangles)))

    def export_off(self, off_filename='model.off'):
        "docstring"
        self.shell()
        f = open(off_filename, 'w')
        f.write('OFF\n')
        f.write('%s %s 0\n' % (len(self.shell_vertices), len(
            self.shell_triangles)))
        for v in self.shell_vertices:
            f.write('%.0f %.0f %.0f\n' % (v[0], v[1], v[2]))
        for p in self.shell_triangles:
            f.write('3')
            for x in p:
                f.write(" %s" % x)
            f.write('\n')
        f.close()

    def insert(self, cuboid):
        "docstring"
        cuboid_id = cuboid.centroid  # id is an instance of Point
        self.cubdict[cuboid_id] = {}
        for orientation, face in cuboid.faces:
            self.cubdict[cuboid_id][orientation] = {
                'face': face,
                'out': True
            }
        x, y, z = cuboid_id.x, cuboid_id.y, cuboid_id.z
        top_id = Point(x, y + 1, z)
        bottom_id = Point(x, y - 1, z)
        west_id = Point(x - 1, y, z)
        east_id = Point(x + 1, y, z)
        north_id = Point(x, y, z - 1)
        south_id = Point(x, y, z + 1)
        if top_id in self.cubdict:
            self.cubdict[top_id]['bottom']['out'] = False
            self.cubdict[cuboid_id]['top']['out'] = False
        if bottom_id in self.cubdict:
            self.cubdict[bottom_id]['top']['out'] = False
            self.cubdict[cuboid_id]['bottom']['out'] = False
        if west_id in self.cubdict:
            self.cubdict[west_id]['east']['out'] = False
            self.cubdict[cuboid_id]['west']['out'] = False
        if east_id in self.cubdict:
            self.cubdict[east_id]['west']['out'] = False
            self.cubdict[cuboid_id]['east']['out'] = False
        if north_id in self.cubdict:
            self.cubdict[north_id]['south']['out'] = False
            self.cubdict[cuboid_id]['north']['out'] = False
        if south_id in self.cubdict:
            self.cubdict[south_id]['north']['out'] = False
            self.cubdict[cuboid_id]['south']['out'] = False


CUBOIDS = dense_cuboids('Node.txt', 'Connectivity.txt', 'density.txt', 0.3)
CUBOID_COMPLEX = CuboidComplex(CUBOIDS)
CUBOID_COMPLEX.export_off()
