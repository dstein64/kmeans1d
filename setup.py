import os
from setuptools import Extension, setup
from setuptools.command.build_ext import build_ext


class BuildExt(build_ext):
    """A custom build extension for adding -std and -stdlib arguments for clang++."""
    def is_using_clang(self):
        cxx = self.compiler.compiler_cxx[0]
        if 'clang' in cxx:
            return True
        # TODO: check if 'cxx' points to clang++.
        return False

    def build_extensions(self):
        if self.is_using_clang():
            for extension in self.extensions:
                # '-std=c++11' is added to `extra_compile_args` so the code can compile
                # with clang++. '-stdlib=libc++' is added to `extra_compile_args` and
                # `extra_link_args` so the code can compile on macOS with Anaconda.
                extension.extra_compile_args.extend(('-std=c++11', '-stdlib=libc++'))
                extension.extra_link_args.append('-stdlib=libc++')
        build_ext.build_extensions(self)


extension = Extension('kmeans1d._core', ['kmeans1d/_core.cpp'])

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
    cmdclass={'build_ext': BuildExt},
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
