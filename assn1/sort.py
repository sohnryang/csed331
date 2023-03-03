import operator
from math import atan2, hypot, pi
from sys import stdin
from typing import Callable, List, Tuple, TypeVar

infast = lambda: stdin.readline().strip()
T = TypeVar("T")


def partition(arr: List[T], lo: int, hi: int, cmp: Callable[[T, T], int]) -> int:
    pivot = arr[lo]
    less_equal_end = lo
    for i in range(lo + 1, hi):
        if cmp(arr[i], pivot) > 0:
            continue
        less_equal_end += 1
        arr[i], arr[less_equal_end] = arr[less_equal_end], arr[i]
    arr[lo], arr[less_equal_end] = arr[less_equal_end], arr[lo]
    return less_equal_end


def quicksort(arr: List[T], cmp: Callable[[T, T], int] = operator.sub) -> None:
    indices: List[Tuple[int, int]] = [(0, len(arr))]
    while indices:
        lo, hi = indices.pop()
        if lo >= hi:
            continue
        pivot_idx = partition(arr, lo, hi, cmp)
        indices.append((lo, pivot_idx))
        indices.append((pivot_idx + 1, hi))


def float_compare(x: float, y: float) -> int:
    if x == y:
        return 0
    elif x < y:
        return -1
    return 1


def compare_points(p1: Tuple[int, int], p2: Tuple[int, int]) -> int:
    angle1 = atan2(*p1)
    if angle1 < 0:
        angle1 += 2 * pi
    angle2 = atan2(*p2)
    if angle2 < 0:
        angle2 += 2 * pi
    if angle1 == angle2:
        return float_compare(hypot(*p1), hypot(*p2))
    return float_compare(angle1, angle2)


if __name__ == "__main__":
    T = int(infast())
    for t in range(T):
        N = int(infast())
        coords = []
        for _ in range(N):
            X, Y = map(int, infast().split())
            coords.append((X, Y))
        quicksort(coords, compare_points)
        for x, y in coords:
            print(x, y)
        if t != T - 1:
            print()
