import ctypes
import os
from typing import List, Sequence, Tuple

import kmeans1d._core

_DLL = ctypes.cdll.LoadLibrary(kmeans1d._core.__file__)

version_txt = os.path.join(os.path.dirname(__file__), 'version.txt')
with open(version_txt, 'r') as f:
    __version__ = f.read().strip()


# TODO: Sort 'array' before clustering, and then unsort.


def cluster(array: Sequence[float], k: int) -> Tuple[List, List]:
    assert k > 0, f'Invalid k: {k}'
    n = len(array)
    assert n > 0, f'Invalid len(array): {n}'
    k = min(k, n)

    c_array = (ctypes.c_double * n)(*array)
    c_n = ctypes.c_ulong(n)
    c_k = ctypes.c_ulong(k)
    c_clusters = (ctypes.c_ulong * n)()
    c_centroids = (ctypes.c_double * k)()

    _DLL.cluster(c_array, c_n, c_k, c_clusters, c_centroids)
    clusters = list(c_clusters)
    centroids = list(c_centroids)
    output = (clusters, centroids)
    return output
