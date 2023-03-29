#include <algorithm>
#include <ios>
#include <iostream>
#include <set>
#include <utility>
#include <vector>

int T, V, E, node_counter;
std::vector<std::vector<std::pair<int, int>>> graph;
std::vector<bool> visited;
std::vector<int> parents;
std::vector<int> node_ids, component_root_ids;
std::set<std::pair<std::pair<int, int>, int>> bridges;

void mark_components(int here) {
  visited[here] = true;
  node_ids[here] = node_counter++;
  component_root_ids[here] = node_ids[here];
  for (int i = 0; i < graph[here].size(); i++) {
    int there = graph[here][i].first;
    if (visited[there]) {
      if (parents[here] != there && component_root_ids[here] > node_ids[there])
        component_root_ids[here] = node_ids[there];
      continue;
    }
    parents[there] = here;
    mark_components(there);
    if (component_root_ids[here] > component_root_ids[there])
      component_root_ids[here] = component_root_ids[there];
  }
}

void collect_bridges(int here) {
  visited[here] = true;
  for (int i = 0; i < graph[here].size(); i++) {
    auto there = graph[here][i];
    if (visited[there.first])
      continue;
    if (node_ids[here] < component_root_ids[there.first]) {
      auto edge = std::make_pair(std::make_pair(std::min(here, there.first),
                                                std::max(here, there.first)),
                                 there.second);
      bridges.insert(edge);
    }
    collect_bridges(there.first);
  }
}

int main() {
  std::ios_base::sync_with_stdio(false);
  std::cin.tie(nullptr);

  std::cin >> T;
  for (int t = 0; t < T; t++) {
    std::cin >> V >> E;
    graph.clear();
    graph.assign(V, {});
    for (int i = 0; i < E; i++) {
      int A, B, L;
      std::cin >> A >> B >> L;
      graph[A].push_back({B, L});
      graph[B].push_back({A, L});
    }
    parents.assign(V, -1);
    visited.assign(V, false);
    node_counter = 0;
    node_ids.assign(V, -1);
    component_root_ids.assign(V, -1);
    mark_components(0);
    visited.assign(V, false);
    bridges.clear();
    collect_bridges(0);
    if (bridges.empty()) {
      std::cout << "-1\n";
      continue;
    }
    std::cout << std::min_element(bridges.begin(), bridges.end(),
                                  [](const auto &v1, const auto &v2) {
                                    return v1.second < v2.second;
                                  })
                     ->second
              << "\n";
  }
  return 0;
}
