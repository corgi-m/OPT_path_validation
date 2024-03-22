import random

import sympy

from model.ABCHelper import ABCHelper


class AtomosHelper(ABCHelper):
    p = None
    q = None
    g = None

    @staticmethod
    def PQPrimeGen(bits=128):
        while True:
            q = sympy.randprime(2 ** (bits - 1), 2 ** bits)
            if sympy.isprime(2 * q + 1):
                return q, 2 * q + 1

    @staticmethod
    def GGen(p, q):
        while True:
            g = random.randint(0, p - 1)  # 随机选择一个 g
            if pow(g, 2, p) != 1 and pow(g, q, p) != 1:
                return g

    @staticmethod
    def SPPrimeGen(g, p, bits=128):
        SK = sympy.randprime(2 ** (bits - 1), 2 ** bits)
        PK = pow(g, SK, p)
        return SK, PK

    @staticmethod
    def RandomGen(bits=128):
        return random.randint(2 ** (bits - 1), 2 ** bits)

    @staticmethod
    def SemiDirect(p, x1, x2):
        a1, b1 = x1
        a2, b2 = x2
        a3 = (a1 + a2) % (p - 1)
        b3 = (a1 + b1 + b2) % (p - 1)
        return a3, b3
