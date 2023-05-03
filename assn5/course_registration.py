from operator import itemgetter
from sys import stdin
from typing import List, Optional, Tuple

infast = lambda: stdin.readline().strip()

T = int(infast())
for _ in range(T):
    N = int(infast())
    C: List[Tuple[int, int]] = []
    for _ in range(N):
        s, e = map(int, infast().split())
        C.append((s, e))
    C.sort(key=itemgetter(1, 0))
    last_course: Optional[Tuple[int, int]] = None
    res = 0
    for s, e in C:
        if last_course is None:
            last_course = (s, e)
            res += 1
            continue
        _, le = last_course
        if s < le:
            continue
        last_course = (s, e)
        res += 1
    print(res)
