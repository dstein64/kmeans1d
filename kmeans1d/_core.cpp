#include <Python.h>

#include <cstdint>
#include <iostream> // TODO: DELETE
#include <limits>
#include <vector>

using namespace std;

typedef unsigned long ulong;

/*
 *  Calculates cluster costs in O(1) using prefix sum arrays.
 */
class CostCalculator {
    vector<double> cumsum;
    vector<double> cumsum2;

  public:
    CostCalculator(double* sorted_array, ulong n) {
        cumsum.push_back(0.0);
        cumsum2.push_back(0.0);
        for (ulong i = 0; i < n; ++i) {
            double x = sorted_array[i];
            cumsum.push_back(x + cumsum[i]);
            cumsum2.push_back(x * x + cumsum2[i]);
        }
    }

    double calc(ulong i, ulong j) {
        if (j < i) return 0.0;
        double mu = (cumsum[j + 1] - cumsum[i]) / (j - i + 1);
        double result = cumsum2[j + 1] - cumsum2[i];
        result += (j - i + 1) * (mu * mu);
        result -= (2 * mu) * (cumsum[j + 1] - cumsum[i]);
        return result;
    }
};

template <typename T>
class Matrix {
    vector<T> data;
    ulong num_rows;
    ulong num_cols;

  public:
    Matrix(ulong num_rows, ulong num_cols) {
        this->num_rows = num_rows;
        this->num_cols = num_cols;
        data.resize(num_rows * num_cols);
    }

    inline T get(ulong i, ulong j) {
        return data[i * num_cols + j];
    }

    inline void set(ulong i, ulong j, T value) {
        data[i * num_cols + j] = value;
    }
};

extern "C" {
void cluster(
        double* sorted_array,
        ulong n,
        ulong k,
        ulong* clusters,
        double* centroids) {
    CostCalculator cost_calculator(sorted_array, n);
    Matrix<double> D(k, n);
    Matrix<ulong> T(k, n);

    for (ulong i = 0; i < n; ++i) {
        D.set(0, i, cost_calculator.calc(0, i));
        T.set(0, i, 0);
    }

    // TODO: REPLACE ALL THE FOLLOWING WITH SMAWK. NO EXPLICIT C MATRIX.
    for (ulong k_ = 1; k_ < k; ++k_) {
        Matrix<double> C(n, n);
        for (ulong i = 0; i < n; ++i) {
            for (ulong j = 0; j < n; ++j) {
                ulong col = i < j - 1 ? i : j - 1; // TODO: underflow? This will ultimately be deleted.
                double x = D.get(k_ - 1, col) + cost_calculator.calc(j, i);
                C.set(i, j, x);
            }
        }
        for (ulong i = 0; i < n; ++i) {
            double min = numeric_limits<double>::infinity();
            ulong argmin = 0;
            for (ulong j = 0; j < n; ++j) {
                double x = C.get(i, j);
                if (x < min) {
                    min = x;
                    argmin = j;
                }
            }
            D.set(k_, i, min);
            T.set(k_, i, argmin);
        }
    }

    // ***************************************************
    // * Extract cluster assignments by backtracking
    // ***************************************************

    // TODO: This is currently O(kn) but can be modified to be O(n).
    //       Details are in section 3 of (Grønlund et al., 2017).

    ulong t = n;
    ulong k_ = k - 1;
    ulong n_ = n - 1;
    // The do/while loop was used in place of:
    //   for (k_ = k - 1; k_ >= 0; --k_)
    // to avoid wraparound of an unsigned type.
    do {
        ulong t_ = t;
        t = T.get(k_, n_);
        double centroid = 0.0;
        for (ulong i = t; i < t_; ++i) {
            clusters[i] = k_;
            centroid += (sorted_array[i] - centroid) / (i - t + 1);
        }
        centroids[k_] = centroid;
        k_ -= 1;
        n_ = t - 1;
    } while (t > 0);
}
} // extern "C"

static PyMethodDef module_methods[] = {
    {NULL, NULL, 0, NULL}
};

static struct PyModuleDef _coremodule = {
    PyModuleDef_HEAD_INIT,
    "kmeans1d._core",
    NULL,
    -1,
    module_methods,
};

PyMODINIT_FUNC PyInit__core(void) {
    return PyModule_Create(&_coremodule);
}
