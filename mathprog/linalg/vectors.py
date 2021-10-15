from math import acos, atan2, cos, pi, sin, sqrt

from mathprog.generic import fraction


def length(vector: tuple):
    return sqrt(sum([c ** 2 for c in vector]))


def add(*vectors: tuple) -> tuple:
    return tuple(map(sum, zip(*vectors)))


def subtract(vector_a: tuple, vector_b: tuple):
    vector_b = tuple([-c for c in vector_b])
    return add(vector_a, vector_b)


def scale(vector: tuple, factor: float):
    return tuple([fraction(c * factor) for c in vector])


def translate(vector: tuple, translation: tuple):
    return add(vector, translation)


def distance(vector_a: tuple, vector_b: tuple):
    return length(subtract(vector_a, vector_b))


def perimeter(vectors: list[tuple]):
    return sum([distance(vectors[i], vectors[(i + 1) % len(vectors)]) for i in range(len(vectors))])


def to_cartesian(polar_vector: tuple):
    length, angle = polar_vector
    return (length * cos(angle), length * sin(angle))


def to_polar(cartesian_vector: tuple):
    x, y = cartesian_vector
    return (length(cartesian_vector), atan2(y, x))


def angle_between(vector_a: tuple, vector_b: tuple):
    """Calculate the angle between two vectors that share a common point"""
    return acos(dot(vector_a, vector_b) / (length(vector_a) * length(vector_b)))


def rotate(vector: tuple, rotation: float):
    polar_vector = to_polar(vector)
    return to_cartesian((polar_vector[0], polar_vector[1] + rotation))


def regular_polygon(n: int):
    """Returns vectors representing an n-sided regular polygon"""
    return [to_cartesian((1, 2 * pi / n * i)) for i in range(n)]


def dot(vector_a: tuple, vector_b: tuple) -> float:
    return sum([a * b for a, b in zip(vector_a, vector_b)])


def cross(vector_a: tuple, vector_b: tuple):
    ax, ay, az = vector_a
    bx, by, bz = vector_b
    return (ay * bz - az * by, az * bx - ax * bz, ax * by - ay * bx)


def unit(vector: tuple):
    return scale(vector, 1 / length(vector))
