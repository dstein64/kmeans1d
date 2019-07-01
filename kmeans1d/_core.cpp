#include <Python.h>

#include <cstdint>
#include <iostream> // TODO: DELETE
#include <limits> // TODO: maybe delete
#include <vector>

using namespace std;

typedef uint32_t u32;

/*
 *  Calculates cluster costs in O(1) using prefix sum arrays.
 */
class CostCalculator {
    vector<double> cumsum;
    vector<double> cumsum2;

  public:
    CostCalculator(double* sorted_array, u32 n) {
        cumsum.push_back(0.0);
        cumsum2.push_back(0.0);
        for (u32 i = 0; i < n; ++i) {
            double x = sorted_array[i];
            cumsum.push_back(x + cumsum[i]);
            cumsum2.push_back(x * x + cumsum2[i]);
        }
    }

    double calc(u32 i, u32 j) {
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
    u32 num_rows;
    u32 num_cols;

  public:
    Matrix(u32 num_rows, u32 num_cols) {
        this->num_rows = num_rows;
        this->num_cols = num_cols;
        data.resize(num_rows * num_cols);
    }

    T get(u32 i, u32 j) {
        return data[i * num_cols + j];
    }

    void set(u32 i, u32 j, T value) {
        data[i * num_cols + j] = value;
    }
};

extern "C" {
void cluster(
        double* sorted_array,
        u32 n,
        u32 k,
        u32* clusters,
        double* centroids) {
    CostCalculator cost_calculator(sorted_array, n);
    Matrix<double> D(k, n);
    Matrix<u32> T(k, n);

    for (u32 i = 0; i < n; ++i) {
        D.set(0, i, cost_calculator.calc(0, i));
        T.set(0, i, 0);
    }

    // TODO: REPLACE ALL THE FOLLOWING WITH SMAWK. NO EXPLICIT C MATRIX.
    for (u32 k_ = 1; k_ < k; ++k_) {
        Matrix<double> C(n, n);
        for (u32 i = 0; i < n; ++i) {
            for (u32 j = 0; j < n; ++j) {
                u32 col = i < j - 1 ? i : j - 1; // TODO: underflow? This will ultimately be deleted.
                double x = D.get(k_ - 1, col) + cost_calculator.calc(j, i);
                C.set(i, j, x);
            }
        }
        for (u32 i = 0; i < n; ++i) {
            double min = numeric_limits<double>::max();
            u32 argmin = 0;
            for (u32 j = 0; j < n; ++j) {
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

    u32 t = n;
    u32 k_ = k - 1;
    u32 n_ = n - 1;
    do {
        u32 t_ = t;
        t = T.get(k_, n_);
        double centroid = 0.0;
        for (u32 i = t; i < t_; ++i) {
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
