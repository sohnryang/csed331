from sys import stdin
from typing import List, Tuple

infast = lambda: stdin.readline().strip()

T = int(infast())
for _ in range(T):
    N, W = map(int, infast().split())
    S: List[Tuple[int, int, int]] = []
    for _ in range(N):
        L, R, Y = map(int, infast().split())
        S.append((L, R, Y))
    arr: List[int] = [0] * W
    for l, r, y in S:
        for x in range(l, r):
            arr[x] = y
    arr.append(0)
    stack: List[int] = []
    res = 0
    for i, y in enumerate(arr):
        while stack and arr[stack[-1]] > arr[i]:
            mid = stack.pop()
            if stack:
                lo = stack[-1]
            else:
                lo = -1
            res = max(res, (i - lo - 1) * arr[mid])
        stack.append(i)
    print(res)
