import os
from setuptools import Extension, setup

extension = Extension('kmeans1d._core', ["kmeans1d/_core.cpp"])

version_txt = os.path.join(os.path.dirname(__file__), 'kmeans1d', 'version.txt')
with open(version_txt, 'r') as f:
    version = f.read().strip()

setup(
    author='Daniel Steinberg',
    author_email='ds@dannyadam.com',
    classifiers=[
          'Development Status :: 4 - Beta',
          'Intended Audience :: Developers',
          'Intended Audience :: Science/Research',
          'Topic :: Scientific/Engineering',
          'Topic :: Scientific/Engineering :: Artificial Intelligence',
          'Topic :: Scientific/Engineering :: Information Analysis',
          'License :: OSI Approved :: MIT License',
          'Operating System :: Unix',
          'Operating System :: POSIX :: Linux',
          'Operating System :: MacOS',
          'Operating System :: Microsoft :: Windows',
          'Programming Language :: Python :: 3',
    ],
    description='A Python package for optimal 1D k-means clustering',
    ext_modules=[extension],
    keywords=['k-means', 'machine learning', 'optimization'],
    license='MIT',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    name='kmeans1d',
    package_data={'kmeans1d': ['version.txt']},
    packages=['kmeans1d'],
    python_requires='>=3.6',
    url='https://github.com/dstein64/kmeans1d',
    version=version,
)
