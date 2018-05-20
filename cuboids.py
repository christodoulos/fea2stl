"A Python library that handles cuboids and cuboid complexes"
import numpy as np
import pymesh
from primitives import Point
from stl import mesh


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

    def export_stl_pymesh(self):
        vertices = np.array(self.shell_vertices)
        faces = np.array(self.shell_triangles)
        stlmesh = pymesh.form_mesh(vertices, faces)
        pymesh.save_mesh('model-pymesh.stl', stlmesh)

    def export_stl(self):
        vertices = np.array(self.shell_vertices)
        faces = np.array(self.shell_triangles)
        stlmesh = mesh.Mesh(np.zeros(faces.shape[0], dtype=mesh.Mesh.dtype))
        for i, f in enumerate(faces):
            for j in range(3):
                stlmesh.vectors[i][j] = vertices[f[j], :]
        stlmesh.save('model.stl')

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
