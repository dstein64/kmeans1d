import os
import setuptools
from setuptools import Extension, setup
from setuptools.command.build_ext import build_ext


class BuildExt(build_ext):
    """A custom build extension for adding -stdlib arguments for clang++."""

    def build_extensions(self):
        # '-std=c++11' is added to `extra_compile_args` so the code can compile
        # with clang++. This works across compilers (ignored by MSVC).
        for extension in self.extensions:
            extension.extra_compile_args.append('-std=c++11')

        try:
            build_ext.build_extensions(self)
        except setuptools.distutils.errors.CompileError:
            # Workaround Issue #2.
            # '-stdlib=libc++' is added to `extra_compile_args` and `extra_link_args`
            # so the code can compile on macOS with Anaconda.
            for extension in self.extensions:
                extension.extra_compile_args.append('-stdlib=libc++')
                extension.extra_link_args.append('-stdlib=libc++')
            build_ext.build_extensions(self)


extension_kmeans = Extension('optimal1Dcluster._core_kmeans', ['optimal1Dcluster/_core_kmeans.cpp'])

version_txt = os.path.join(os.path.dirname(__file__), 'optimal1Dcluster', 'version.txt')
with open(version_txt, 'r') as f:
    version = f.read().strip()

with open('README.md') as f:
    long_description = f.read()

setup(
    author='Jan Meißner',
    author_email='philipp.meissner@rwth-aachen.de',
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
    cmdclass={'build_ext': BuildExt},
    description='A Python package for optimal 1D clustering',
    ext_modules=[extension_kmeans],
    keywords=['k-means', 'k-median', 'machine learning', 'optimization'],
    license='MIT',
    long_description=long_description,
    long_description_content_type='text/markdown',
    name='optimal1Dcluster',
    package_data={'optimal1Dcluster': ['version.txt']},
    packages=['optimal1Dcluster'],
    python_requires='>=3.6',
    url='',
    version=version,
)
