import math
from numbers import Real


class Calculator:
    @staticmethod
    def _number(value):
        if isinstance(value, bool) or not isinstance(value, Real):
            raise TypeError("Expected a real number")
        if not math.isfinite(value):
            raise ValueError("Expected a finite number")
        return value

    def add(self, a, b):
        return self._number(a) + self._number(b)

    def subtract(self, a, b):
        return self._number(a) - self._number(b)

    def multiply(self, a, b):
        return self._number(a) * self._number(b)

    def divide(self, a, b):
        a, b = self._number(a), self._number(b)
        if b == 0:
            raise ZeroDivisionError("Division by zero")
        return a / b

    @staticmethod
    def is_prime_number(number):
        if isinstance(number, bool) or not isinstance(number, int):
            raise TypeError("Expected an integer")
        if number < 2:
            return False
        return all(number % divisor for divisor in range(2, math.isqrt(number) + 1))
