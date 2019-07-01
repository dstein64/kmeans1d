from setuptools import Extension, setup

extension = Extension('kmeans1d._core', ["kmeans1d/_core.cpp"])

# TODO: optimization flag for compiler
# TODO: special handling for windows?

setup(name='kmeans1d',
      packages=['kmeans1d'],
      ext_modules=[extension])
