import  os
from os.path import join as pjoin
from setuptools import setup, Extension
import subprocess
import sys
import numpy

AMGX_DIR = os.environ.get('AMGX_DIR')
AMGX_BUILD_DIR = os.environ.get('AMGX_BUILD_DIR')
MPI_DIR = os.environ.get('MPI_HOME')

if not AMGX_DIR:
    # look in PREFIX:
    PREFIX = sys.prefix
    if os.path.isfile(os.path.join(PREFIX, 'lib/libamgxsh.so')):
        AMGX_lib_dirs = [os.path.join(PREFIX, 'lib')]
        AMGX_include_dirs = [os.path.join(PREFIX, 'include')]
    else:
        raise EnvironmentError('AMGX_DIR not set and libamgxsh.so not found')
else:
    if not AMGX_BUILD_DIR:
        AMGX_BUILD_DIR = os.path.join(AMGX_DIR, 'build')
    AMGX_lib_dirs = [AMGX_BUILD_DIR]
    AMGX_include_dirs = [
        os.path.join(AMGX_DIR, 'include'),
        os.path.join(AMGX_DIR, 'include')
    ]

if not MPI_DIR:
    PREFIX = sys.prefix
    if os.path.isfile(os.path.join(PREFIX, 'lib/libmpi.so')):
        MPI_include_dirs = [os.path.join(PREFIX, 'include')]
        MPI_lib_dirs = [os.path.join(PREFIX, 'lib')]
    else:
        log.info("MPI_HOME not found")
else:
    MPI_include_dirs = [os.path.join(MPI_DIR, 'include')]
    MPI_lib_dirs = [os.path.join(MPI_DIR, 'lib')]


from Cython.Build import cythonize
ext = cythonize([
    Extension(
        'pyamgx',
        sources=['pyamgx/pyamgx.pyx'],
        depends=['pyamgx/*.pyx, pyamgx/*.pxi'],
        libraries=['amgxsh'],
        language='c',
        include_dirs = [
            numpy.get_include(),
        ] + AMGX_include_dirs
        + MPI_include_dirs,
        library_dirs = [
            numpy.get_include(),
        ] + AMGX_lib_dirs
        + MPI_lib_dirs,
        runtime_library_dirs = [
            numpy.get_include(),
        ] + AMGX_lib_dirs
        + MPI_lib_dirs,
)])

setup(name='pyamgx',
      author='Ashwin Srinath, Tadd Bindas',
      version='0.2.2',
      ext_modules = ext,
      zip_safe=False)
