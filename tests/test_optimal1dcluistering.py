import unittest

from optimal1dclustering import cluster

import numpy as np
import math
from collections import Counter


def _get_calculate_median_cluster_cost(min_cluster_size=0):
    def calculate_median_cluster_cost(x, i, j):
        """
        the min_cluster_size property does not destroy monge concavity
        to proof for any u<v and a<b: cost(v,b)+cost(u,a) <= cost(u,b)+cost(v,a)
        assume v>a then cost(v,a) is infinity as it violates the min_cluster_size requirement.
                    hence the condition holds
        assume v<=a then we have u<v<=a<b it now follows that because if cost(v,b) or cost(u,a) is infinity due to
               it having a too small cluster size cost(v,a) must also have a too small cluster size (due to b-v >= a-v
               and a-u >= a-v) hence the inequeality reduces to inf <= inf which is true. For all other cases the costs
               are finite and the standard proofs from the paper hold.
        """

        if i > j:
            raise ValueError("Invalid cluster range")
        if j - i + 1 < min_cluster_size:
            return float("inf")
        m_i_j = (j + i) / 2
        centroid = (x[int(np.floor(m_i_j))] + x[int(np.ceil(m_i_j))]) / 2
        cost = sum(abs(x[k] - centroid) for k in range(i, j + 1))
        return cost

    return calculate_median_cluster_cost


def _get_calculate_mean_cluster_cost(min_cluster_size=0):
    def calculate_mean_cluster_cost(x, i, j):
        if i > j:
            raise ValueError("Invalid cluster range")
        if j - i + 1 < min_cluster_size:
            return float("inf")
        cluster_mean = np.mean(x[i: j + 1])
        cost = sum((x[k] - cluster_mean) ** 2 for k in range(i, j + 1))
        return cost

    return calculate_mean_cluster_cost


def _slow_1d_optimal(x, k, calculate_cluster_cost):
    """
    Slow O(k*n^2) implementation of the dynamic program.
    """
    sorted_x, sorted_indices = zip(*sorted((val, idx) for idx, val in enumerate(x)))

    n = len(sorted_x)
    D = np.zeros((k + 1, n + 1)) + float("inf")
    T = np.zeros((k + 1, n + 1), dtype=int)

    # Base case
    for m in range(1, n + 1):
        D[1][m] = calculate_cluster_cost(sorted_x, 0, m - 1)

    # DP to fill D and T
    for i in range(2, k + 1):
        for m in range(1, n + 1):
            for j in range(1, m + 1):
                cost = D[i - 1][j - 1] + calculate_cluster_cost(sorted_x, j - 1, m - 1)
                if cost < D[i][m]:
                    D[i][m] = cost
                    T[i][m] = j

    if math.isinf(D[k][n]):
        raise ValueError("No valid clustering exists, this happens if k > len(x) or min_cluster_size*k > len(x) if it is set.")

    # Backtrack to find the optimal clusters
    clusters = []
    current = n
    for i in range(k, 0, -1):
        start = T[i][current]
        lower = max(0, start - 1)
        clusters.extend(
            [i,] * (current - lower)
        )
        current = lower

    clusters.reverse()

    _, clusters_original_order = zip(*sorted(zip(sorted_indices, clusters)))
    return list(clusters_original_order)


def cluster_baseline(x, k, min_cluster_size=0, mode=2):
    """Naive O(k*n^2) dynamic program."""
    if mode == 2:
        return _slow_1d_optimal(x, k, _get_calculate_mean_cluster_cost(min_cluster_size))
    else:
        return _slow_1d_optimal(x, k, _get_calculate_median_cluster_cost(min_cluster_size))


def are_clusterings_equivalent(cluster1, cluster2):
    label_mapping = dict(zip(cluster1, cluster2))
    relabeled_cluster1 = [label_mapping[label] for label in cluster1]
    return relabeled_cluster1 == cluster2


def min_cluster_size(numbers):
    return min(Counter(numbers).values()) if numbers else 0


class TestKmeans1D(unittest.TestCase):
    """kmeans1d tests"""

    def test_cluster(self):
        x = [4.0, 4.1, 4.2, -50, 200.2, 200.4, 200.9, 80, 100, 102]
        k = 4
        clusters, centroids = cluster(x, k)
        self.assertEqual(clusters, [1, 1, 1, 0, 3, 3, 3, 2, 2, 2])
        self.assertEqual(centroids, [-50.0, 4.1, 94.0, 200.5])

    def test_cluster_empty_array(self):
        with self.assertRaises(ValueError):
            cluster([], 1)

    def test_cluster_k_greater_than_array_length(self):
        with self.assertRaises(ValueError):
            cluster([1.0, 2.0], 3)

    def test_cluster_invalid_k(self):
        with self.assertRaises(ValueError):
            cluster([1.0, 2.0], 0)

    def test_cluster_invalid_mode(self):
        with self.assertRaises(ValueError):
            cluster([1.0, 2.0, 3.0], 2, mode=0)

    def test_cluster_min_cluster_size_too_large(self):
        with self.assertRaises(ValueError):
            cluster([1.0, 2.0, 3.0, 4.0], 2, min_cluster_size=3)

    def test_large_array_with_different_k(self):
        np.random.seed(42)
        large_array = np.random.rand(1000)
        k_values = [2, 3, 10, 20]
        for k in k_values:
            clusters, _ = cluster(large_array, k)
            self.assertEqual(len(set(clusters)), k, f"Failed for k={k}")

    def test_large_array_with_min_cluster_size(self):
        np.random.seed(42)
        large_array = np.array([10] * 130 + [20] * 20 + [30] * 5) + 0.01 * np.random.rand(155)  # 3 clusters
        k = 3
        min_sizes = [5, 10, 50]
        for min_size in min_sizes:
            clusters, _ = cluster(large_array, k, min_cluster_size=min_size)
            self.assertTrue(
                min_cluster_size(clusters) >= min_size,
                f"Failed for min_cluster_size={min_size}",
            )
            self.assertEqual(len(set(clusters)), k, f"Failed for k={k}")

    def test_cluster_equivalence_with_baseline(self):
        np.random.seed(42)
        array = np.random.rand(60) * 100
        for k in range(1, 6):  # small k values due to baseline's computational cost
            for min_cluster_size in [0, 2, 5]:
                for mode in [1, 2]:
                    clusters, _ = cluster(array, k, min_cluster_size=min_cluster_size, mode=mode)
                    baseline_clusters = cluster_baseline(array.tolist(), k, min_cluster_size=min_cluster_size, mode=mode)
                    self.assertTrue(
                        are_clusterings_equivalent(clusters, baseline_clusters),
                        f"Failed for k={k}, min_cluster_size={min_cluster_size}, mode={mode}",
                    )

    def test_median_vs_mean_clustering(self):
        array = [1, 2, 3, 4, 40, 41, 100]
        k = 2
        clusters_mean, _ = cluster(array, k, mode=2)
        clusters_median, _ = cluster(array, k, mode=1)
        self.assertNotEqual(
            clusters_mean,
            clusters_median,
            "Mean and median clustering should differ for this array",
        )


if __name__ == "__main__":
    unittest.main()
