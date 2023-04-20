from collections import defaultdict
from math import inf
from sys import stdin
from typing import DefaultDict, List, Set, Tuple, Union
import heapq

Vertex = Tuple[int, bool]
Edge = Tuple[Union[int, float], Vertex]

infast = lambda: stdin.readline().strip()

T = int(infast())
for _ in range(T):
    V, E = map(int, infast().split())
    graph: DefaultDict[Vertex, Set[Edge]] = defaultdict(set)
    for _ in range(E):
        u, v, p = map(int, infast().split())
        graph[(u, False)].add((p, (v, False)))
        graph[(u, False)].add((0, (v, True)))
        graph[(u, True)].add((p, (v, True)))
    dist: DefaultDict[Vertex, Union[int, float]] = defaultdict(lambda: inf)
    dist[(0, False)] = 0
    pq: List[Edge] = []
    heapq.heappush(pq, (0, (0, False)))
    while pq:
        here_dist, here = heapq.heappop(pq)
        if here_dist > dist[here]:
            continue
        for weight, there in graph[here]:
            if dist[here] + weight < dist[there]:
                dist[there] = dist[here] + weight
                heapq.heappush(pq, (dist[there], there))
    res = min(dist[(V - 1, False)], dist[(V - 1, True)])
    if res == inf:
        print(-1)
    else:
        print(res)
