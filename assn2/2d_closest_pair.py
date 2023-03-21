import operator
from sys import stdin
from typing import List, Tuple

infast = lambda: stdin.readline().strip()
INF = 2**64


def dist(p1: Tuple[int, int], p2: Tuple[int, int]) -> int:
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])


def min_dist(lo: int, hi: int) -> int:
    n = hi - lo + 1
    if n == 3:
        return min(
            dist(P[lo], P[lo + 1]), dist(P[lo], P[lo + 2]), dist(P[lo + 1], P[lo + 2])
        )
    elif n == 2:
        return dist(P[lo], P[lo + 1])
    elif n < 2:
        return INF
    mid = (lo + hi) // 2
    midpoint = P[mid]
    left_min = min_dist(lo, mid)
    right_min = min_dist(mid + 1, hi)
    strip_radius = min(left_min, right_min)
    strip: List[Tuple[int, int]] = []
    for p in P[lo : hi + 1]:
        if abs(p[0] - midpoint[0]) < strip_radius:
            strip.append(p)
    strip.sort(key=operator.itemgetter(1))
    res = min(left_min, right_min)
    for i, p1 in enumerate(strip):
        for p2 in strip[i + 1 : i + 12]:
            res = min(res, dist(p1, p2))
    return res


T = int(infast())
P: List[Tuple[int, int]] = []
for _ in range(T):
    P.clear()
    N = int(infast())
    for _ in range(N):
        X, Y = map(int, infast().split())
        P.append((X, Y))
    P.sort()
    print(min_dist(0, N - 1))
