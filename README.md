[![Build Status](https://github.com/jan-meissner/optimal1dclustering/workflows/build/badge.svg)](https://github.com/jan-meissner/optimal1dclustering/actions)

optimal1dclustering
========
Add *k*-medians and add a minimum cluster size parameter to https://github.com/dstein64/kmeans1d.

A Python library with an implementation of *k*-means and *k*-medians clustering on 1D data, based on the algorithm
from Xiaolin (1991), as presented by Gronlund et al. (2017, Section 2.2).

The algorithm implemented in this library can also find the optimal clustering when clusters are required to have a 
minimum cluster size. It still finds the optimal clustering as the cost function is still monge concave.

Globally optimal clustering is NP-hard for multi-dimensional data. Lloyd's algorithm is a
popular approach for finding a locally optimal solution. For 1-dimensional data, there are polynomial
time algorithms. The algorithm implemented here is an *O(kn + n log n)* dynamic programming algorithm
for finding the globally optimal *k* clusters for *n* 1D data points.

The code is written in C++, and wrapped with Python.

Requirements
------------

*optimal1dclustering* supports Python 3.x.

Installation
------------

[optimal1dclustering](https://pypi.python.org/pypi/optimal1dclustering) is available on PyPI, the Python Package Index.

```sh
$ pip3 install optimal1dclustering
```

Example Usage
-------------

```python
import optimal1dclustering

x = [4.0, 4.1, 4.2, -50, 200.2, 200.4, 200.9, 80, 100, 102]
k = 4 # Number of clusters
min_cluster_size = 2 # The minimum number of elements in each cluster
mode = 2 # 2 for k-means; 1 for k-medians

clusters, centroids = optimal1dclustering.cluster(x, k, min_cluster_size = min_cluster_size, mode = mode)

print(clusters)   # [0, 1, 1, 0, 3, 3, 3, 2, 2, 2]
print(centroids)  # [-23.0, 4.15, 94.0, 200.5]
```

Tests
-----

Tests are in [tests/](https://github.com/jan-meissner/optimal1dclustering/blob/master/tests).

```sh
# Run tests
$ python3 -m unittest discover tests -v
```

Development
-----------

The underlying C++ code can be built in-place, outside the context of `pip`. This requires Python
development tools for building Python modules (e.g., the `python3-dev` package on Ubuntu). `gcc`,
`clang`, and `MSVC` have been tested.

```
$ python3 setup.py build_ext --inplace
```

The [packages](https://github.com/jan-meissner/optimal1dclustering/blob/master/.github/workflows/packages.yml)
GitHub action can be manually triggered (`Actions` > `packages` > `Run workflow`) to build wheels
and a source distribution.

License
-------

The code in this repository has an [MIT License](https://en.wikipedia.org/wiki/MIT_License).

See [LICENSE](https://github.com/jan-meissner/optimal1dclustering/blob/master/LICENSE).

References
----------

[1] Wu, Xiaolin. "Optimal Quantization by Matrix Searching." Journal of Algorithms 12, no. 4
(December 1, 1991): 663

[2] Gronlund, Allan, Kasper Green Larsen, Alexander Mathiasen, Jesper Sindahl Nielsen, Stefan Schneider,
and Mingzhou Song. "Fast Exact K-Means, k-Medians and Bregman Divergence Clustering in 1D."
ArXiv:1701.07204 [Cs], January 25, 2017. http://arxiv.org/abs/1701.07204.
