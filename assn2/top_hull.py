import heapq
from collections import defaultdict
from sys import stdin
from typing import DefaultDict, List, Optional, Tuple

LineInfo = Tuple[int, int, int]
SortableLineInfo = Tuple[int, int, int]
ResultInfo = Tuple[int, int, Optional[int]]
infast = lambda: stdin.readline().strip()


def to_sortable(line: LineInfo) -> SortableLineInfo:
    return (-line[1], line[0], line[2])


T = int(infast())
for _ in range(T):
    N = int(infast())
    lines_by_start: DefaultDict[int, List[LineInfo]] = defaultdict(list)
    lines_by_finish: DefaultDict[int, List[LineInfo]] = defaultdict(list)
    for _ in range(N):
        L, R, H = map(int, infast().split())
        lines_by_start[L].append((L, H, R))
        lines_by_finish[R].append((L, H, R))

    endpoints = set(lines_by_start.keys()) | set(lines_by_finish.keys())
    res: List[ResultInfo] = []
    highest_lines: List[SortableLineInfo] = []
    lines_to_delete: List[SortableLineInfo] = []
    for event_point in sorted(endpoints):
        if event_point in lines_by_finish:
            finished_lines = lines_by_finish[event_point]
            for finished_line in finished_lines:
                heapq.heappush(lines_to_delete, to_sortable(finished_line))
            while lines_to_delete:
                if lines_to_delete[0] == highest_lines[0]:
                    heapq.heappop(lines_to_delete)
                    heapq.heappop(highest_lines)
                else:
                    break
            if res:
                if not highest_lines:
                    new_height = None
                else:
                    new_height = highest_lines[0][0]
                current_result_line = res[-1]
                if new_height is None:
                    res.pop()
                    res.append(
                        (current_result_line[0], current_result_line[1], event_point)
                    )
                elif new_height != current_result_line[1]:
                    res.pop()
                    res.append(
                        (current_result_line[0], current_result_line[1], event_point)
                    )
                    res.append((event_point, new_height, None))

        if event_point in lines_by_start:
            started_lines = lines_by_start[event_point]
            for started_line in started_lines:
                heapq.heappush(highest_lines, to_sortable(started_line))
            new_height = highest_lines[0][0]
            if not res:
                res.append((event_point, new_height, None))
                continue
            current_result_line = res[-1]
            if current_result_line[2] is not None:
                res.append((event_point, new_height, None))
                continue
            if new_height != current_result_line[1]:
                res.pop()
                res.append(
                    (current_result_line[0], current_result_line[1], event_point)
                )
                res.append((event_point, new_height, None))

    merged_result: List[ResultInfo] = []
    for line in res:
        if line[2] is not None and line[2] - line[0] <= 0:
            continue
        if not merged_result:
            merged_result.append(line)
            continue
        last_line = merged_result[-1]
        if last_line[1] == line[1] and last_line[2] == line[0]:
            merged_result.pop()
            merged_result.append((last_line[0], last_line[1], line[2]))
        else:
            merged_result.append(line)
    printed_result = []
    for result_line in merged_result:
        L, H, R = result_line
        if R is None:
            continue
        print(L, R, -H)
