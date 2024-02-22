from collections import namedtuple
import ctypes
import os
from typing import Sequence

import optimal1dclustering._core  # type: ignore


Clustered = namedtuple("Clustered", "clusters centroids")

_DLL = ctypes.cdll.LoadLibrary(optimal1dclustering._core.__file__)

version_txt = os.path.join(os.path.dirname(__file__), "version.txt")
with open(version_txt, "r") as f:
    __version__ = f.read().strip()


def cluster(array: Sequence[float], k: int, min_cluster_size: int = 0, mode: int = 2) -> Clustered:
    """
    Clusters a sequence of floats into `k` clusters, using either the k-means or k-medians algorithm,
    optionally enforcing a minimum cluster size.

    Args:
        array (Sequence[float]): A sequence of floats to be clustered.
        k (int): Number of clusters.
        min_cluster_size (int, optional): Minimum size of each cluster. Defaults to 0, implying no minimum.
        mode (int, optional): Determines the distance metric to use.
                              - 2 for k-means, which minimizes the sum of squared Euclidean distances
                                (L2 norm) to the cluster centroids.
                              - 1 for k-medians, which minimizes the sum of Manhattan distances
                                (L1 norm) to the cluster medians.

    Returns:
        Tuple containing arrays `clusters` and `centroids`.

    Note:
        Implementation is heavily based on https://github.com/dstein64/kmeans1d.

    References:
            Allan Grønlund, Kasper Green Larsen, Alexander Mathiasen, Jesper Sindahl Nielsen, Stefan Schneider, and
            Mingzhou Song. 2017. Fast exact k-means, k-medians and Bregman divergence clustering in 1D.
            arXiv preprint arXiv:1701.07204.
    """
    n = len(array)
    if k <= 0 or n == 0:
        raise ValueError("Invalid parameters: k must be > 0 and array must not be empty.")

    if k > n:
        raise ValueError("Invalid clustering: k cannot be greater than the length of the array.")

    if min_cluster_size * k > n:
        raise ValueError(
            "Invalid clustering: The product of min_cluster_size and k cannot be greater than the length of the array."
        )

    if not (mode == 1 or mode == 2):
        raise ValueError("The mode must be 1 or 2.")

    c_array = (ctypes.c_double * n)(*array)
    c_n = ctypes.c_ulong(n)
    c_k = ctypes.c_ulong(k)
    c_clusters = (ctypes.c_ulong * n)()
    c_centroids = (ctypes.c_double * k)()

    _DLL.cluster(c_array, c_n, c_k, c_clusters, c_centroids, min_cluster_size, mode == 2)
    clusters = list(c_clusters)
    centroids = list(c_centroids)

    output = Clustered(clusters=clusters, centroids=centroids)

    return output
