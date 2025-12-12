import unittest
import warnings

class TestKmeans1D(unittest.TestCase):
    """kmeans1d tests"""
    def test(self):
        with warnings.catch_warnings(record=True) as caught_warnings:
            warnings.simplefilter('always')

            # Import here to catch warnings. E.g.:
            # RuntimeWarning("The global interpreter lock (GIL) has been enabled to load module
            # 'kmeans1d._core', which has not declared that it can run safely without the GIL...")
            from kmeans1d import cluster

            x = [4.0, 4.1, 4.2, -50, 200.2, 200.4, 200.9, 80, 100, 102]
            k = 4
            clusters, centroids = cluster(x, k)
            self.assertEqual(clusters, [1, 1, 1, 0, 3, 3, 3, 2, 2, 2])
            self.assertEqual(centroids, [-50.0, 4.1, 94.0, 200.5])

            self.assertEqual(len(caught_warnings), 0, f'Warnings were raised: {caught_warnings}')

if __name__ == '__main__':
    unittest.main()
