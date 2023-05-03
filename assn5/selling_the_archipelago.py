from sys import stdin, setrecursionlimit
from typing import Dict, List, Set, Tuple, Union

setrecursionlimit(10000)
infast = lambda: stdin.readline().strip()
EdgeLen = Union[int, float]
SortableEdgeInfo = Tuple[EdgeLen, Tuple[int, int]]


class UnionFind:
    def __init__(self, N: int) -> None:
        self.set_size = [1] * N
        self.num_sets = N
        self.rank = [0] * N
        self.parents = [0] * N
        for i in range(N):
            self.parents[i] = i

    def find_set(self, i: int) -> int:
        if self.parents[i] != i:
            self.parents[i] = self.find_set(self.parents[i])
            return self.parents[i]
        return i

    def same_set(self, i, j: int) -> bool:
        return self.find_set(i) == self.find_set(j)

    def union_set(self, i: int, j: int) -> None:
        if self.same_set(i, j):
            return
        self.num_sets -= 1
        x = self.find_set(i)
        y = self.find_set(j)
        if self.rank[x] > self.rank[y]:
            self.parents[x] = y
            self.set_size[x] += self.set_size[y]
        else:
            self.parents[y] = x
            self.set_size[y] += self.set_size[x]
            if self.rank[x] == self.rank[y]:
                self.rank[y] += 1


T = int(infast())
for _ in range(T):
    I, P, B = map(int, infast().split())
    initials = list(map(int, infast().split()))
    edges: List[SortableEdgeInfo] = []
    for _ in range(B):
        I1, I2, C = map(int, infast().split())
        edges.append((C, (I1, I2)))
    edges.sort()
    single_root = UnionFind(I)
    for v in initials:
        single_root.union_set(v, initials[0])
    components = UnionFind(I)
    for edge in edges:
        _, (u, v) = edge
        if single_root.same_set(u, v):
            continue
        single_root.union_set(u, v)
        components.union_set(u, v)
    bridge_edges: List[SortableEdgeInfo] = []
    component_ids: Set[int] = set()
    for edge in edges:
        c, (u, v) = edge
        if components.same_set(u, v):
            continue
        u_comp = components.find_set(u)
        v_comp = components.find_set(v)
        component_ids.add(u_comp)
        component_ids.add(v_comp)
        bridge_edges.append((-c, (u_comp, v_comp)))
    compressed_ids: Dict[int, int] = dict()
    id_count = 0
    for component_id in sorted(component_ids):
        if component_id in compressed_ids:
            continue
        compressed_ids[component_id] = id_count
        id_count += 1
    bridge_edges.sort()
    res = 0
    merged_comps = UnionFind(components.num_sets)
    for edge in bridge_edges:
        c, (u_comp, v_comp) = edge
        u = compressed_ids[u_comp]
        v = compressed_ids[v_comp]
        if merged_comps.same_set(u, v):
            continue
        merged_comps.union_set(u, v)
        res -= c
    print(res)
