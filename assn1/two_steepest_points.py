from fractions import Fraction
from sys import stdin

infast = lambda: stdin.readline().strip()

T = int(infast())
for _ in range(T):
    N = int(infast())
    coords = []
    for _ in range(N):
        X, Y = map(int, infast().split())
        coords.append((X, Y))
    coords.sort()
    max_slope = None
    res = None
    for p1, p2 in zip(coords[:-1], coords[1:]):
        slope = abs(Fraction(p2[1] - p1[1], p2[0] - p1[0]))
        if max_slope is None or slope > max_slope:
            max_slope = slope
            res = [p1, p2]
    print(res[0][0], res[0][1], res[1][0], res[1][1])  # type: ignore
