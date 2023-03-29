from collections import deque
from sys import stdin
from typing import Deque, List, Set, Tuple

infast = lambda: stdin.readline().strip()


def available(pos: Tuple[int, int], min_speed: int) -> bool:
    y, x = pos
    return 0 <= y < N and 0 <= x < M and G[y][x] >= min_speed


def adjacents(pos: Tuple[int, int]) -> List[Tuple[int, int]]:
    y, x = pos
    return [(y - 1, x), (y, x - 1), (y, x + 1), (y + 1, x)]


def check_arrival(min_speed: int) -> bool:
    if not available((0, 0), min_speed):
        return False
    q: Deque[Tuple[int, int]] = deque()
    q.append((0, 0))
    visited: Set[Tuple[int, int]] = set()
    while q:
        here = q.popleft()
        if here == (N - 1, M - 1):
            return True
        for there in adjacents(here):
            if not available(there, min_speed):
                continue
            if there in visited:
                continue
            visited.add(there)
            q.append(there)
    return False


T = int(infast())
for _ in range(T):
    N, M = map(int, infast().split())
    G: List[List[int]] = []
    speeds: Set[int] = set()
    for y in range(N):
        line = [int(x) for x in infast().split()]
        speeds = speeds | set(line)
        G.append(line)
    speeds_list = list(speeds)
    speeds_list.sort()
    lo = 0
    hi = len(speeds_list) - 1
    while lo + 1 < hi:
        mid = (lo + hi) // 2
        if check_arrival(speeds_list[mid]):
            lo = mid
        else:
            hi = mid
    if check_arrival(speeds_list[hi]):
        print(speeds_list[hi])
    else:
        print(speeds_list[lo])
