#include <algorithm>
#include <cstring>
#include <ios>
#include <iostream>
#include <vector>

int T, N, K, dp[5100][5100], depths[5100];
std::vector<std::vector<int>> children;

void dfs(int here, int depth) {
  depths[here] = depth;
  for (const auto &there : children[here]) {
    if (depths[there] != -1)
      continue;
    dfs(there, depth + 1);
  }
}

int minimum_k(int root, int last_storage, int max_len) {
  int &res = dp[root][last_storage];
  if (res != -1)
    return res;
  res = 1;
  for (const auto &child : children[root])
    res += minimum_k(child, root, max_len);
  if (depths[root] - depths[last_storage] <= max_len) {
    int res2 = 0;
    for (const auto &child : children[root])
      res2 += minimum_k(child, last_storage, max_len);
    res = std::min(res, res2);
  }
  return res;
}

int main() {
  std::ios_base::sync_with_stdio(false);
  std::cin.tie(nullptr);

  std::cin >> T;
  for (int t = 0; t < T; t++) {
    std::cin >> N >> K;
    children.assign(N, {});
    for (int i = 0; i < N - 1; i++) {
      int U, V;
      std::cin >> U >> V;
      children[U].push_back(V);
    }
    if (N == K) {
      std::cout << 0 << "\n";
      continue;
    }
    memset(depths, -1, sizeof(depths));
    dfs(0, 0);

    int lo = 0, hi = *std::max_element(depths, depths + N);
    while (lo + 1 < hi) {
      memset(dp, -1, sizeof(dp));
      int mid = (lo + hi) / 2, res = 1;
      for (const auto &root_child : children[0])
        res += minimum_k(root_child, 0, mid);
      if (res > K)
        lo = mid;
      else
        hi = mid;
    }
    std::cout << hi << "\n";
  }
}
