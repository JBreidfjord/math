from __future__ import annotations

import math


class Complex:
    def __init__(self, real, imag):
        self.real = real
        self.imag = imag

    def conjugate(self):
        return Complex(self.real, -self.imag)

    def inverse(self):
        return Complex(
            self.real / (self.real ** 2 + self.imag ** 2),
            -self.imag / (self.real ** 2 + self.imag ** 2),
        )

    def to_polar(self):
        return abs(self), math.atan2(self.imag, self.real)

    @classmethod
    def from_polar(cls, r, theta):
        return cls(r * math.cos(theta), r * math.sin(theta))

    def principal(self):
        ...

    def roots(self, n: int):
        assert n > 0
        assert isinstance(n, int)

        s, phi = self.to_polar()
        r = s ** (1 / n)
        theta = [(phi + 2 * math.pi * k) / n for k in range(n)]
        return [Complex.from_polar(r, t) for t in theta]

    def __repr__(self):
        if self.imag < 0:
            return f"{self.real} - {-self.imag}i"
        else:
            return f"{self.real} + {self.imag}i"

    def __add__(self, other: Complex | int | float):
        if isinstance(other, Complex):
            return Complex(self.real + other.real, self.imag + other.imag)
        elif isinstance(other, (int, float)):
            return Complex(self.real + other, self.imag)
        else:
            raise TypeError(
                f"unsupported operand type(s) for +: '{type(self).__name__}' and '{type(other).__name__}'"
            )

    def __sub__(self, other: Complex | int | float):
        if isinstance(other, Complex):
            return Complex(self.real - other.real, self.imag - other.imag)
        elif isinstance(other, (int, float)):
            return Complex(self.real - other, self.imag)
        else:
            raise TypeError(
                f"unsupported operand type(s) for -: '{type(self).__name__}' and '{type(other).__name__}'"
            )

    def __mul__(self, other: Complex | int | float):
        if isinstance(other, Complex):
            return Complex(
                self.real * other.real - self.imag * other.imag,
                self.real * other.imag + self.imag * other.real,
            )
        elif isinstance(other, (int, float)):
            return Complex(self.real * other, self.imag * other)
        else:
            raise TypeError(
                f"unsupported operand type(s) for *: '{type(self).__name__}' and '{type(other).__name__}'"
            )

    def __div__(self, other: Complex | int | float):
        if isinstance(other, Complex):
            return Complex(
                (self.real * other.real + self.imag * other.imag)
                / (other.real ** 2 + other.imag ** 2),
                (self.imag * other.real - self.real * other.imag)
                / (other.real ** 2 + other.imag ** 2),
            )
        elif isinstance(other, (int, float)):
            return Complex(self.real / other, self.imag / other)
        else:
            raise TypeError(
                f"unsupported operand type(s) for /: '{type(self).__name__}' and '{type(other).__name__}'"
            )

    def __truediv__(self, other: Complex | int | float):
        return self.__div__(other)

    def __abs__(self):
        return math.sqrt(self.real ** 2 + self.imag ** 2)

    def __pow__(self, other: int):
        if isinstance(other, int):
            if other == 0:
                return Complex(1, 0)
            elif other == 1:
                return self
            else:
                return self.__pow__(other - 1) * self
        else:
            raise TypeError(
                f"unsupported operand type(s) for pow: '{type(self).__name__}' and '{type(other).__name__}'"
            )

    def __neg__(self):
        return Complex(-self.real, -self.imag)

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        else:
            return math.isclose(self.real, other.real, abs_tol=1e-1) and math.isclose(
                self.imag, other.imag, abs_tol=1e-1
            )

    def __ne__(self, other):
        return not self.__eq__(other)
