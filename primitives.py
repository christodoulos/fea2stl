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
