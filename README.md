kmeans1d
========

A Python library with an implementation of *k*-means clustering on 1D data, based on the algorithm
in (Xiaolin 1991), as presented in section 2.2 of (Gronlund et al., 2017).

Globally optimal *k*-means clustering is NP-hard for multi-dimensional data. LLoyd's algorithm is a
popular approach for finding a locally optimal solution. For 1-dimensional data, there are polynomial time
algorithms. The algorithm implemented here is a *O(kn + n log n)* dynamic programming algorithm for finding
the globally optimal *k* clusters for *n* 1D data points.

The code is written in C++, and wrapped with Python.

Requirements
------------

*kmeans1d* supports Python 3.x.

Installation
------------

[kmeans1d](https://pypi.python.org/pypi/kmeans1d) is available on PyPI, the Python Package Index.

```sh
$ pip3 install kmeans1d
```

Example Usage
-------------

```python
import kmeans1d

x = [4.0, 4.1, 4.2, -50, 200.2, 200.4, 200.9, 80, 100, 102]
k = 4

clusters, centroids = kmeans1d.cluster(x, k)

print(clusters)   # [1, 1, 1, 0, 3, 3, 3, 2, 2, 2]
print(centroids)  # [-50.0, 4.1, 94.0, 200.5]

```

License
-------

The code in this repository has an [MIT License](https://en.wikipedia.org/wiki/MIT_License).

See [LICENSE](https://github.com/dstein64/kmeans1d/blob/master/LICENSE).

References
----------

[1] Wu, Xiaolin. "Optimal Quantization by Matrix Searching." Journal of Algorithms 12, no. 4
(December 1, 1991): 663

[2] Gronlund, Allan, Kasper Green Larsen, Alexander Mathiasen, Jesper Sindahl Nielsen, Stefan Schneider,
and Mingzhou Song. "Fast Exact K-Means, k-Medians and Bregman Divergence Clustering in 1D."
ArXiv:1701.07204 [Cs], January 25, 2017. http://arxiv.org/abs/1701.07204.