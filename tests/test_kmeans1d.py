import unittest

from kmeans1d import cluster

class TestKmeans1D(unittest.TestCase):
    """kmeans1d tests"""
    def test_cluster(self):
        x = [4.0, 4.1, 4.2, -50, 200.2, 200.4, 200.9, 80, 100, 102]
        k = 4
        clusters, centroids = cluster(x, k)
        self.assertEqual(clusters, [1, 1, 1, 0, 3, 3, 3, 2, 2, 2])
        self.assertEqual(centroids, [-50.0, 4.1, 94.0, 200.5])


if __name__ == '__main__':
    unittest.main()
