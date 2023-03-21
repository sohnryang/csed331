#include <algorithm>
#include <ios>
#include <iostream>
#include <vector>

int T, N;
std::vector<int> A;

#ifdef DEBUG
void print_vec(const std::vector<int> &arr) {
  std::cout << "[ ";
  for (auto &v : arr)
    std::cout << v << " ";
  std::cout << "]\n";
}
#endif

constexpr int median_idx(int len) {
  if (len % 2 == 0)
    return len / 2 - 1;
  return len / 2;
}

int get_kth(const std::vector<int> &arr, int k) {
#ifdef DEBUG
  print_vec(arr);
  std::cout << "k=" << k << "\n";
#endif
  if (arr.size() <= 5) {
    std::vector<int> copied(arr);
    std::sort(copied.begin(), copied.end());
    return copied[k];
  }
  std::vector<std::vector<int>> less_than_median, greater_than_median;
  std::vector<int> medians;
  for (int i = 0; i < arr.size(); i += 5) {
    std::vector<int> subarr;
    for (int j = 0; j < 5 && i + j < arr.size(); j++)
      subarr.push_back(arr[i + j]);
    std::sort(subarr.begin(), subarr.end());
    less_than_median.push_back({});
    for (int j = 0; j < median_idx(subarr.size()); j++)
      less_than_median.back().push_back(subarr[j]);
    medians.push_back(subarr[median_idx(subarr.size())]);
    greater_than_median.push_back({});
    for (int j = median_idx(subarr.size()) + 1; j < subarr.size(); j++)
      greater_than_median.back().push_back(subarr[j]);
  }
  int median_of_medians = get_kth(medians, median_idx(medians.size()));
  std::vector<int> left_partition, right_partition;
  int duplicate_median_count = 0;
  for (auto &v : arr) {
    if (v == median_of_medians)
      duplicate_median_count++;
    else if (v < median_of_medians)
      left_partition.push_back(v);
    else
      right_partition.push_back(v);
  }
  if (left_partition.size() <= k &&
      k < left_partition.size() + duplicate_median_count)
    return median_of_medians;
  else if (k < left_partition.size())
    return get_kth(left_partition, k);
  return get_kth(right_partition,
                 k - left_partition.size() - duplicate_median_count);
}

int main() {
  std::ios_base::sync_with_stdio(false);
  std::cin.tie(nullptr);
  std::cin >> T;
  for (int t = 0; t < T; t++) {
    A.clear();
    std::cin >> N;
    A.assign(N, 0);
    for (int i = 0; i < N; i++)
      std::cin >> A[i];
    std::cout << get_kth(A, median_idx(A.size())) << "\n";
  }
  return 0;
}
