import pytest
import random
from fea2stl import Point, Vector


@pytest.fixture
def random_coordinates():
    x = random.random()
    y = random.random()
    z = random.random()
    return {"x": x, "y": y, "z": z}


def test_primitives_method0():
    x = Point(1, 2, 3)
    y = Point(4, 5, 6)
    assert x - y == Vector(3, 3, 3), "test 0 failed"


def test_primitives_method1():
    x = Point(1, 2, 3)
    y = Point(4, 5, 6)
    z = Vector(3, 3, 3)
    assert x + z == y, "test 1 failed"


def test_primitives_method2(random_coordinates):
    coords = random_coordinates
    x = Point(coords["x"], coords["y"], coords["z"])
    y = Point(coords["x"], coords["y"], coords["z"])
    z = x - y
    assert x + z == y, "test 2 failed"
