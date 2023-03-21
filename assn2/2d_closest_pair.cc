#include <algorithm>
#include <cassert>
#include <ios>
#include <iostream>
#include <limits>
#include <utility>
#include <vector>

using Point = std::pair<long long, long long>;

int T, N;
std::vector<Point> P;

constexpr long long dist(const Point &p1, const Point &p2) {
  return abs(p1.first - p2.first) + abs(p1.second - p2.second);
}

long long min_dist(int lo, int hi) {
  int n = hi - lo + 1;
  if (n == 3)
    return std::min({dist(P[lo], P[lo + 1]), dist(P[lo], P[lo + 2]),
                     dist(P[lo + 1], P[lo + 2])});
  else if (n == 2)
    return dist(P[lo], P[lo + 1]);
  else if (n < 2)
    return std::numeric_limits<long long>::max();
  int mid = (lo + hi) / 2;
  Point midpoint = P[mid];
  long long left_min = min_dist(lo, mid), right_min = min_dist(mid + 1, hi),
            strip_radius = std::min(left_min, right_min);
  std::vector<Point> strip;
  for (int i = lo; i <= hi; i++)
    if (abs(P[i].first - midpoint.first) < strip_radius)
      strip.push_back(P[i]);
  std::sort(strip.begin(), strip.end(),
            [](auto &left, auto &right) { return left.second < right.second; });
  long long res = strip_radius;
  for (int i = 0; i < strip.size(); i++)
    for (int j = i + 1; j < strip.size() && j <= i + 11; j++)
      res = std::min(res, dist(strip[i], strip[j]));
  return res;
}

int main() {
  std::ios_base::sync_with_stdio(false);
  std::cin.tie(nullptr);
  std::cin >> T;
  for (int t = 0; t < T; t++) {
    std::cin >> N;
    P.clear();
    for (int i = 0; i < N; i++) {
      long long X, Y;
      std::cin >> X >> Y;
      P.push_back({X, Y});
    }
    std::sort(P.begin(), P.end());
    std::cout << min_dist(0, P.size() - 1) << "\n";
  }
  return 0;
}
