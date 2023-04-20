from collections import defaultdict
from enum import Enum
from math import inf
from sys import stdin
from typing import DefaultDict, List, Optional, Set, Tuple, Union
from pprint import pprint
import heapq

infast = lambda: stdin.readline().strip()


class VertexType(Enum):
    REAL = 0
    EXPRESS_GATE_IN = 1
    EXPRESS_GATE_OUT = 2


EXPRESS_GATE_OUT = (99_999, VertexType.EXPRESS_GATE_OUT)


Vertex = Tuple[int, VertexType]
EdgeLen = Union[int, float]
Edge = Tuple[EdgeLen, Vertex, bool]

T = int(infast())
for _ in range(T):
    graph: DefaultDict[Vertex, Set[Edge]] = defaultdict(set)
    express_srcs: Set[Vertex] = set()
    express_dests: Set[Vertex] = set()
    N, M = map(int, infast().split())
    s, t = map(int, infast().split())
    for _ in range(M):
        U, V, L, E = map(int, infast().split())
        src = (U, VertexType.REAL)
        dest = (V, VertexType.REAL)
        if E:
            express_srcs.add(src)
            express_dests.add(dest)
        graph[src].add((L, dest, bool(E)))
    dist_first_pass: DefaultDict[Vertex, EdgeLen] = defaultdict(lambda: inf)
    pq: List[Edge] = []
    dist_first_pass[(0, VertexType.REAL)] = 0
    heapq.heappush(pq, (0, (0, VertexType.REAL), False))
    while pq:
        here_dist, here, _ = heapq.heappop(pq)
        if here_dist > dist_first_pass[here]:
            continue
        for weight, there, is_express in graph[here]:
            if is_express:
                continue
            if dist_first_pass[here] + weight < dist_first_pass[there]:
                dist_first_pass[there] = dist_first_pass[here] + weight
                heapq.heappush(pq, (dist_first_pass[there], there, False))
    graph_with_gates: DefaultDict[Vertex, Set[Edge]] = defaultdict(set)
    for dest in express_dests:
        graph_with_gates[EXPRESS_GATE_OUT].add((0, dest, False))
    for src in express_srcs:
        arrival_time = dist_first_pass[src]
        if arrival_time == inf:
            continue
        wait_time = s - arrival_time
        express_in = (src[0], VertexType.EXPRESS_GATE_IN)
        if wait_time <= 0:
            if arrival_time > t:
                continue
            graph_with_gates[src].add((0, express_in, False))
            graph_with_gates[express_in].add(
                (t - s + wait_time, EXPRESS_GATE_OUT, False)
            )
        else:
            graph_with_gates[src].add((wait_time, express_in, False))
            graph_with_gates[express_in].add((t - s, EXPRESS_GATE_OUT, False))
    for here, edges in graph.items():
        for edge in edges:
            weight, there, is_express = edge
            if is_express:
                graph_with_gates[(here[0], VertexType.EXPRESS_GATE_IN)].add(edge)
            else:
                graph_with_gates[here].add(edge)
    pq.clear()
    dist: DefaultDict[Vertex, EdgeLen] = defaultdict(lambda: inf)
    parent: DefaultDict[Vertex, Optional[Vertex]] = defaultdict(lambda: None)
    dist[(0, VertexType.REAL)] = 0
    heapq.heappush(pq, (0, (0, VertexType.REAL), False))
    while pq:
        here_dist, here, _ = heapq.heappop(pq)
        if here_dist > dist[here]:
            continue
        for weight, there, _ in graph_with_gates[here]:
            if dist[here] + weight < dist[there]:
                dist[there] = dist[here] + weight
                parent[there] = here
                heapq.heappush(pq, (dist[there], there, False))
    dest = (N - 1, VertexType.REAL)
    here = dest
    print(parent)
    print(dist)
    print(dist_first_pass)
    pprint(graph_with_gates)
    while here != (0, VertexType.REAL):
        if here is None or here[1] == VertexType.EXPRESS_GATE_OUT:
            break
        here = parent[here]
    else:
        print(dist[dest])
        continue
    if dist_first_pass[dest] == inf:
        print(-1)
    else:
        print(dist_first_pass[dest])
