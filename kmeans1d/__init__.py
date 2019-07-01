import ctypes
from typing import List, Sequence, Tuple

import kmeans1d._core

_DLL = ctypes.cdll.LoadLibrary(kmeans1d._core.__file__)

_UINT32_MAX = 0xffffffff


def cluster(array: Sequence[float], k: int) -> Tuple[List, List]:
    # TODO: Sort 'array'

    assert 0 < k <= _UINT32_MAX, f'Invalid k: {k}'
    n = len(array)

    assert 0 < n <= _UINT32_MAX, f'Invalid len(array): {n}'
    assert k <= n, f'Invalid k: {k}, len(array): {n}'

    c_array = (ctypes.c_double * n)(*array)
    c_n = ctypes.c_uint32(n)
    c_k = ctypes.c_uint32(k)
    c_clusters = (ctypes.c_uint32 * n)()
    c_centroids = (ctypes.c_double * k)()

    _DLL.cluster(c_array, c_n, c_k, c_clusters, c_centroids)
    clusters = list(c_clusters)
    centroids = list(c_centroids)
    output = (clusters, centroids)
    return output
