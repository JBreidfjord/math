import math
import re

from mathprog.linalg import vectors as vec


def linear_combination(scalars: list, *vectors: tuple):
    scaled = [vec.scale(v, s) for v, s in zip(vectors, scalars)]
    return vec.add(*scaled)


def multiply_by_vector(matrix: tuple[tuple], vector: tuple) -> tuple:
    return linear_combination(vector, *zip(*matrix))


def scale(matrix: tuple[tuple], scalar: tuple):
    new_mtx = [vec.scale(row, scalar) for row in matrix]
    return tuple(new_mtx)


def matrix_multiply(matrix_a: tuple[tuple], matrix_b: tuple[tuple]):
    return tuple(tuple(vec.dot(row, col) for col in zip(*matrix_b)) for row in matrix_a)


def transpose(matrix: tuple[tuple]):
    return tuple(zip(*matrix))


def det(matrix: tuple[tuple]):
    if len(matrix[0]) == 1:
        return matrix[0]
    elif len(matrix[0]) == 2:
        return matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]
    else:
        return sum([v * cofactor(matrix, 1, j) for j, v in enumerate(matrix[0], 1)])


def minor(matrix: tuple[tuple], i: int, j: int):
    i -= 1  # Shift to index
    j -= 1

    # Creates new matrix without row & column matching i & j
    new_matrix = []
    for m, row in enumerate(matrix):
        if m == i:
            continue
        new_row = []
        for n, column in enumerate(row):
            if n != j:
                new_row.append(column)
        new_matrix.append(tuple(new_row))
    return det(tuple(new_matrix))


def cofactor(matrix: tuple[tuple], i: int, j: int):
    m = minor(matrix, i, j)
    return m if (i + j) % 2 == 0 else -m


def cofactor_matrix(matrix: tuple[tuple]):
    cof_mtx = []
    for i in range(1, len(matrix) + 1):
        cof_row = []
        for j in range(1, len(matrix[0]) + 1):
            cof_row.append(cofactor(matrix, i, j))
        cof_mtx.append(tuple(cof_row))
    return tuple(cof_mtx)


def adjugate(matrix: tuple[tuple]):
    return transpose(cofactor_matrix(matrix))


def inverse(matrix: tuple[tuple]):
    return scale(adjugate(matrix), 1 / det(matrix))


def from_string(text: str):
    text = re.sub("−", "-", text)
    text = re.sub("[^0-9-]", " ", text).strip()
    ins = text.split()
    size = int(math.sqrt(len(ins)))
    matrix = [[None] * size for _ in range(size)]
    j = 0
    for i, v in enumerate(ins):
        i = i % size
        matrix[i][j] = int(v)
        if i == size - 1:
            j += 1
    matrix = [tuple(row) for row in matrix]
    return tuple(matrix)

