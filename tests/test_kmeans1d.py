from concurrent.futures import ThreadPoolExecutor
import sys
import sysconfig
import textwrap
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
            expected_clusters = [1, 1, 1, 0, 3, 3, 3, 2, 2, 2]
            expected_centroids = [-50.0, 4.1, 94.0, 200.5]

            clusters, centroids = cluster(x, k)
            self.assertEqual(clusters, expected_clusters)
            self.assertEqual(centroids, expected_centroids)

            # Next, use multithreading so that thread-safety is checked under free-threaded Python.

            num_threads = 4
            iterations_per_thread = 100000

            def run():
                for _ in range(iterations_per_thread):
                    clusters, centroids = cluster(x, k)
                    self.assertEqual(clusters, expected_clusters)
                    self.assertEqual(centroids, expected_centroids)

            with ThreadPoolExecutor(max_workers=num_threads) as executor:
                futures = [executor.submit(run) for _ in range(num_threads)]
                [f.result() for f in futures]  # this will raise exceptions in the main thread

            self.assertEqual(len(caught_warnings), 0, f'Warnings were raised: {caught_warnings}')

    def test_abi3t_build(self):
        from kmeans1d.core import _DLL

        # Free-threaded Python 3.15+ should use abi3t. Otherwise, it falls back to a
        # version-specific build.
        if sysconfig.get_config_var('Py_GIL_DISABLED') != 1 or sys.version_info < (3, 15):
            self.skipTest('Not free-threaded Python 3.15+')
        self.assertTrue(hasattr(_DLL, 'PyModExport__core'))

    def test_subinterpreters(self):
        # Per-interpreter GILs are supported on Python 3.12+, but this test uses
        # concurrent.interpreters, which requires Python 3.14.
        if sys.version_info < (3, 14):
            self.skipTest('concurrent.interpreters is not available')

        from concurrent import interpreters

        code = textwrap.dedent('''
            from kmeans1d import cluster
            x = [4.0, 4.1, 4.2, -50, 200.2, 200.4, 200.9, 80, 100, 102]
            for _ in range(10000):
                clusters, centroids = cluster(x, 4)
                assert clusters == [1, 1, 1, 0, 3, 3, 3, 2, 2, 2], clusters
                assert centroids == [-50.0, 4.1, 94.0, 200.5], centroids
        ''')

        def run():
            interpreter = interpreters.create()
            try:
                interpreter.exec(code)
            finally:
                interpreter.close()

        # Use multiple interpreters in parallel, since per-interpreter GILs don't share a lock.
        num_interpreters = 4
        with ThreadPoolExecutor(max_workers=num_interpreters) as executor:
            futures = [executor.submit(run) for _ in range(num_interpreters)]
            [f.result() for f in futures]  # this will raise exceptions in the main thread

if __name__ == '__main__':
    unittest.main()
