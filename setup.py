import os

from setuptools import setup
from pybind11.setup_helpers import Pybind11Extension


setup(ext_modules=[Pybind11Extension(
    "dlsym", ["ext/dlsym.cpp"], cxx_std=11,
    libraries={"posix": ["dl"], "nt": ["psapi"]}[os.name],
)])
