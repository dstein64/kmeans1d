import os
import sys
import sysconfig

import setuptools
from setuptools import Extension, setup
from setuptools.command.build_ext import build_ext

# Free-threaded builds support the Stable ABI (abi3t) as of Python 3.15 (PEP 803), which
# setuptools supports as of version 84.2. This follows the abi3t migration guide:
#   https://docs.python.org/3/howto/abi3t-migration.html
free_threaded = sysconfig.get_config_var('Py_GIL_DISABLED') == 1
setuptools_version = tuple(int(x) for x in setuptools.__version__.split('.')[:2])
use_stable_abi = not free_threaded or (
    sys.version_info >= (3, 15) and setuptools_version >= (84, 2)
)

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
            # Work around Issue #2.
            # '-stdlib=libc++' is added to `extra_compile_args` and `extra_link_args`
            # so the code can compile on macOS with Anaconda.
            for extension in self.extensions:
                extension.extra_compile_args.append('-stdlib=libc++')
                extension.extra_link_args.append('-stdlib=libc++')
            build_ext.build_extensions(self)


extension_kwargs = {}
if use_stable_abi:
    # We use Python's Stable ABI so that one wheel works across Python minor release versions
    # (e.g., 3.7 and 3.8, but not 4.0). Here we specify the minimum supported version. On
    # GIL-enabled Python, Py_LIMITED_API selects abi3. On free-threaded Python, Py_TARGET_ABI3T
    # selects abi3t. The resulting cp315-abi3.abi3t wheel is compatible with both free-threaded and
    # GIL-enabled builds of Python 3.15 and later.
    stable_abi_macro = 'Py_TARGET_ABI3T' if free_threaded else 'Py_LIMITED_API'
    if free_threaded:
        stable_abi_major, stable_abi_minor = 3, 15
    elif sys.version_info >= (3, 12):
        # Subinterpreters with their own GIL require targeting Python 3.12.
        stable_abi_major, stable_abi_minor = 3, 12
    else:
        stable_abi_major, stable_abi_minor = 3, 2
    extension_kwargs['define_macros'] = [(
        stable_abi_macro, f'0x{stable_abi_major:02x}{stable_abi_minor:02x}0000'
    )]
    # setuptools uses py_limited_api for both abi3 and abi3t.
    extension_kwargs['py_limited_api'] = True
extension = Extension('kmeans1d._core', ['kmeans1d/_core.cpp'], **extension_kwargs)

version_txt = os.path.join(os.path.dirname(__file__), 'kmeans1d', 'version.txt')
with open(version_txt, 'r') as f:
    version = f.read().strip()

with open('README.md') as f:
    long_description = f.read()

setup_options = {}
if use_stable_abi:
    setup_options['bdist_wheel'] = {
        'py_limited_api': f'cp{stable_abi_major}{stable_abi_minor}'
    }
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
    long_description=long_description,
    long_description_content_type='text/markdown',
    name='kmeans1d',
    options=setup_options,
    package_data={'kmeans1d': ['version.txt']},
    packages=['kmeans1d'],
    python_requires='>=3.6',
    url='https://github.com/dstein64/kmeans1d',
    version=version,
)
