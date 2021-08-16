# from setuptools import setup
# from Cython.Build import cythonize
# import numpy

# def make_setup(path_dir):
#     return setup(
#         ext_modules = cythonize(path_dir),
#         include_dirs=[numpy.get_include()]
#     )

from distutils.core import setup
from Cython.Build import cythonize
import numpy

setup(ext_modules = cythonize("Utils/*.pyx"),
    include_dirs=[numpy.get_include()]
)

