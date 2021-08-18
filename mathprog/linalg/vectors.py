from math import atan2, cos, pi, sin, sqrt


def length(vector: tuple):
    return sqrt(vector[0] ** 2 + vector[1] ** 2)


def add(*vectors: tuple) -> tuple:
    return (sum([v[0] for v in vectors]), sum([v[1] for v in vectors]))


def subtract(vector_a: tuple, vector_b: tuple):
    return add(vector_a, (-vector_b[0], -vector_b[1]))


def scale(vector: tuple, factor: float):
    return (vector[0] * factor, vector[1] * factor)


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


def angle_between(vector_a: tuple, vector_b: tuple, common: tuple):
    """Calculate the angle between two vectors that share a common point"""
    a = subtract(vector_a, common)
    b = subtract(vector_b, common)
    angle = abs(atan2(b[1], b[0]) - atan2(a[1], a[0]))
    return angle if angle <= pi else 2 * pi - angle


def rotate(vector: tuple, rotation: float):
    polar_vector = to_polar(vector)
    return to_cartesian((polar_vector[0], polar_vector[1] + rotation))


def regular_polygon(n: int):
    """Returns vectors representing an n-sided regular polygon"""
    return [to_cartesian((1, 2 * pi / n * i)) for i in range(n)]
