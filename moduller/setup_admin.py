from setuptools import setup
from Cython.Build import cythonize

setup(
    name="genelgeler",
    ext_modules=cythonize(["genelgeler.py"], compiler_directives={'language_level': "3"})
)
