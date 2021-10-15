import math
import random

import numpy as np


def fraction(x: float):
    best_tol = np.inf
    best_i = None
    best_j = None
    for i in range(1000, -1000, -1):
        if i == 0:
            continue
        for j in range(1000, -1000, -1):
            if j == 0:
                continue
            if math.isclose(i / j, x, rel_tol=1e-3):
                if abs(x - i / j) < best_tol or (abs(i) < abs(best_i) and abs(j) < abs(best_j)):
                    best_tol = abs(x - i / j)
                    best_i = i
                    best_j = j

    if best_i is None or best_j is None:
        return 0
    elif best_j == 1 or best_j == -1:
        return best_i * best_j
    elif best_i < 0 and best_j < 0:
        return f"{-best_i}/{-best_j}"
    return f"{best_i}/{best_j}"


def roots(coeffs: tuple):
    # Not finished
    def f(x: float):
        y = 0
        for i, coeff in enumerate(coeffs, 1):
            y += coeff * x ** (len(coeffs) - i)
        return y

    def df(x: float):
        y = 0
        d_coeffs = tuple(coeff * (len(coeffs) - i) for i, coeff in enumerate(coeffs, 1))[:-1]
        for i, d_coeff in enumerate(d_coeffs, 1):
            y += d_coeff * x ** (len(d_coeffs) - i)
        return y

    x = random.randint(-100, 100)  # Random starting value
    y = f(x)
    while not np.isclose(y, 0):
        x -= f(x) / df(x)
        y = f(x)
    return x
