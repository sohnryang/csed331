from sys import stdin
from typing import Tuple

infast = lambda: stdin.readline().strip()

Mat3X3 = Tuple[Tuple[int, int, int], Tuple[int, int, int], Tuple[int, int, int]]
MOD = 1000000000


def matmul(a: Mat3X3, b: Mat3X3) -> Mat3X3:
    res = []
    for i in range(3):
        row = []
        for j in range(3):
            entry = 0
            for k in range(3):
                entry += a[i][k] * b[k][j]
                entry %= MOD
            row.append(entry)
        res.append(tuple(row))
    return tuple(res)


def matpow(mat: Mat3X3, exponent: int) -> Mat3X3:
    if exponent == 0:
        return ((1, 0, 0), (0, 1, 0), (0, 0, 1))
    sqrted = matpow(mat, exponent // 2)
    if exponent % 2 == 0:
        return matmul(sqrted, sqrted)
    else:
        return matmul(matmul(sqrted, sqrted), mat)


T = int(infast())


for _ in range(T):
    N = int(infast())
    if N == 1:
        print(2)
        continue
    powed = matpow(((3, 1, -1), (1, 0, 0), (0, 1, 0)), N - 2)
    print((7 * powed[0][0] + 2 * powed[0][1] + powed[0][2]) % MOD)
