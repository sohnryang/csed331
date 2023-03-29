#include <algorithm>
#include <cstdint>
#include <functional>
#include <ios>
#include <iostream>
#include <queue>
#include <tuple>
#include <unordered_map>
#include <unordered_set>
#include <vector>

using LineInfo = std::tuple<int64_t, int64_t, int64_t>;
using SortableLineInfo = std::tuple<int64_t, int64_t, int64_t>;
using ResultInfo = std::tuple<int64_t, int64_t, int64_t>;
using LinePQ =
    std::priority_queue<SortableLineInfo, std::vector<SortableLineInfo>,
                        std::greater<SortableLineInfo>>;

constexpr SortableLineInfo to_sortable(const LineInfo &line) {
  return {-std::get<1>(line), std::get<0>(line), std::get<2>(line)};
}

int main() {
  std::ios_base::sync_with_stdio(false);
  std::cin.tie(nullptr);
  int T;
  std::cin >> T;
  for (int t = 0; t < T; t++) {
    int N;
    std::unordered_map<int, std::vector<LineInfo>> lines_by_start,
        lines_by_finish;
    std::cin >> N;
    for (int i = 0; i < N; i++) {
      int L, R, H;
      std::cin >> L >> R >> H;
      if (!lines_by_start.count(L))
        lines_by_start[L] = {};
      lines_by_start[L].push_back({L, H, R});
      if (!lines_by_finish.count(R))
        lines_by_finish[R] = {};
      lines_by_finish[R].push_back({L, H, R});
    }
    std::unordered_set<int> endpoint_set;
    for (auto &endpoint_info : lines_by_start)
      endpoint_set.insert(endpoint_info.first);
    for (auto &endpoint_info : lines_by_finish)
      endpoint_set.insert(endpoint_info.first);
    std::vector<int64_t> endpoints(endpoint_set.begin(), endpoint_set.end());
    std::sort(endpoints.begin(), endpoints.end());
    std::vector<ResultInfo> res;
    LinePQ highest_lines, lines_to_delete;
    for (const auto &event_point : endpoints) {
      if (lines_by_finish.count(event_point)) {
        for (const auto &finished_line : lines_by_finish[event_point])
          lines_to_delete.push(to_sortable(finished_line));
        while (!lines_to_delete.empty()) {
          if (lines_to_delete.top() != highest_lines.top())
            break;
          lines_to_delete.pop();
          highest_lines.pop();
        }
        if (!res.empty()) {
          int64_t new_height;
          if (highest_lines.empty())
            new_height = -1;
          else
            new_height = std::get<0>(highest_lines.top());
          ResultInfo current_result_line = res.back();
          if (new_height == -1) {
            res.pop_back();
            res.push_back({std::get<0>(current_result_line),
                           std::get<1>(current_result_line), event_point});
          } else if (new_height != std::get<1>(current_result_line)) {
            res.pop_back();
            res.push_back({std::get<0>(current_result_line),
                           std::get<1>(current_result_line), event_point});
            res.push_back({event_point, new_height, -1});
          }
        }
      }
      if (lines_by_start.count(event_point)) {
        for (const auto &started_line : lines_by_start[event_point])
          highest_lines.push(to_sortable(started_line));
        int64_t new_height = std::get<0>(highest_lines.top());
        if (res.empty()) {
          res.push_back({event_point, new_height, -1});
          continue;
        }
        ResultInfo current_result_line = res.back();
        if (std::get<2>(current_result_line) != -1) {
          res.push_back({event_point, new_height, -1});
          continue;
        }
        if (new_height != std::get<1>(current_result_line)) {
          res.pop_back();
          res.push_back({std::get<0>(current_result_line),
                         std::get<1>(current_result_line), event_point});
          res.push_back({event_point, new_height, -1});
        }
      }
    }
    std::vector<ResultInfo> merged_result;
    for (const auto &line : res) {
      if (std::get<2>(line) != -1 && std::get<2>(line) - std::get<0>(line) <= 0)
        continue;
      if (merged_result.empty()) {
        merged_result.push_back(line);
        continue;
      }
      ResultInfo last_line = merged_result.back();
      if (std::get<1>(last_line) == std::get<1>(line) &&
          std::get<2>(last_line) == std::get<0>(line)) {
        merged_result.pop_back();
        merged_result.push_back({std::get<0>(last_line), std::get<1>(last_line),
                                 std::get<2>(line)});
      } else
        merged_result.push_back(line);
    }
    for (const auto &result_line : merged_result) {
      if (std::get<2>(result_line) == -1)
        continue;
      std::cout << std::get<0>(result_line) << " " << std::get<2>(result_line)
                << " " << -std::get<1>(result_line) << "\n";
    }
  }
  return 0;
}
