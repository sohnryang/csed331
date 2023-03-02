import operator
from sys import stdin

infast = lambda: stdin.readline().strip()


def psum(arr):
    res = [arr[0]]
    for x in arr[1:]:
        res.append(res[-1] + x)
    return res


T = int(infast())
for _ in range(T):
    N = int(infast())
    coords = []
    for i in range(N):
        X, Y = map(int, infast().split())
        coords.append((X, Y, i))
    x_sorted = list(sorted(coords, key=operator.itemgetter(0)))
    y_sorted = list(sorted(coords, key=operator.itemgetter(1)))
    x_sorted_idx = [0] * N
    y_sorted_idx = [0] * N
    for i, (_, _, j) in enumerate(x_sorted):
        x_sorted_idx[j] = i
    for i, (_, _, j) in enumerate(y_sorted):
        y_sorted_idx[j] = i
    x_psum = psum([x[0] for x in x_sorted])
    y_psum = psum([x[1] for x in y_sorted])
    res = None
    for x, y, id in coords:
        i = x_sorted_idx[id]
        x_sum_left = x * i - x_psum[i - 1] if i != 0 else 0
        x_sum_right = (x_psum[-1] - x_psum[i]) - x * (N - i - 1)
        j = y_sorted_idx[id]
        y_sum_up = y * j - y_psum[j - 1] if j != 0 else 0
        y_sum_down = (y_psum[-1] - y_psum[j]) - y * (N - j - 1)
        current_res = x_sum_left + x_sum_right + y_sum_up + y_sum_down
        if res is None:
            res = current_res
        else:
            res = min(res, current_res)
    print(res)
