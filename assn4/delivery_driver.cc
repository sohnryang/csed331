#include <algorithm>
#include <cstdint>
#include <cstring>
#include <ios>
#include <iostream>
#include <unordered_map>
#include <unordered_set>
#include <utility>
#include <vector>

int64_t T, N, M, S, E, K;
int64_t cache[4001][4001];
const int64_t MOD = 20230419;
std::vector<std::vector<int64_t>> graph;
std::vector<int64_t> topological_sorted, visit_order;
std::vector<bool> visited;
std::unordered_set<int64_t> D;

void dfs(int64_t here) {
  visited[here] = true;
  for (const auto &there : graph[here]) {
    if (visited[there])
      continue;
    dfs(there);
  }
  topological_sorted.push_back(here);
}

int64_t count_paths(int64_t here, int64_t dest) {
  int64_t &res = cache[here][dest];
  if (res != -1)
    return res;
  if (here == dest)
    return 1;
  res = 0;
  for (const auto &there : graph[here]) {
    res += count_paths(there, dest);
    res %= MOD;
  }
  return res;
}

int main() {
  std::ios_base::sync_with_stdio(false);
  std::cin.tie(nullptr);
  std::cin >> T;
  for (int64_t t = 0; t < T; t++) {
    std::cin >> N >> M;
    graph.assign(N, {});
    for (int64_t i = 0; i < M; i++) {
      int64_t U, V;
      std::cin >> U >> V;
      graph[U].push_back(V);
    }
    std::cin >> S >> E >> K;
    memset(cache, -1, sizeof(cache));
    if (K == 0) {
      std::cout << count_paths(S, E) << '\n';
      continue;
    }
    D.clear();
    for (int64_t i = 0; i < K; i++) {
      int64_t d;
      std::cin >> d;
      D.insert(d);
    }
    visited.assign(N, false);
    topological_sorted.clear();
    dfs(S);
    std::reverse(topological_sorted.begin(), topological_sorted.end());
    visit_order.clear();
    for (const auto &node : topological_sorted)
      if (D.count(node))
        visit_order.push_back(node);
    if (visit_order.size() != K) {
      std::cout << "0\n";
      continue;
    }
    int64_t res = count_paths(S, visit_order[0]);
    for (int64_t i = 1; i < visit_order.size(); i++) {
      int64_t src = visit_order[i - 1], dest = visit_order[i];
      res *= count_paths(src, dest);
      res %= MOD;
    }
    res *= count_paths(visit_order.back(), E);
    res %= MOD;
    std::cout << res << '\n';
  }
  return 0;
}
