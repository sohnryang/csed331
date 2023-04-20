from collections import defaultdict
from math import inf
from sys import stdin
from typing import DefaultDict, List, Set, Tuple, Union
import heapq

infast = lambda: stdin.readline().strip()


Vertex = Tuple[int, bool]
EdgeLen = Union[int, float]
Edge = Tuple[EdgeLen, Vertex, bool]

T = int(infast())
for _ in range(T):
    graph: DefaultDict[Vertex, Set[Edge]] = defaultdict(set)
    N, M = map(int, infast().split())
    s, t = map(int, infast().split())
    for _ in range(M):
        U, V, L, E = map(int, infast().split())
        graph[(U, False)].add((L, (V, False), bool(E)))
    dist: DefaultDict[Vertex, EdgeLen] = defaultdict(lambda: inf)
    pq: List[Edge] = []
    dist[(0, False)] = 0
    heapq.heappush(pq, (0, (0, False), False))
    while pq:
        here_dist, here, _ = heapq.heappop(pq)
        if here_dist > dist[here]:
            continue
        took_break = here[1]
        if here_dist < s and not took_break:
            there = (here[0], True)
            wait_time = s - here_dist
            if dist[here] + wait_time < dist[there]:
                dist[there] = dist[here] + wait_time
                heapq.heappush(pq, (dist[there], there, False))
        for weight, there, is_express in graph[(here[0], False)]:
            if is_express and not (
                s <= here_dist <= t and s <= here_dist + weight <= t
            ):
                continue
            if dist[here] + weight < dist[there]:
                dist[there] = dist[here] + weight
                heapq.heappush(pq, (dist[there], there, False))
    res = min(dist[(N - 1, True)], dist[(N - 1, False)])
    if res == inf:
        print(-1)
    else:
        print(res)
