import ctypes
from ctypes import CFUNCTYPE, POINTER, c_char_p, c_double, c_int
import importlib
import math
import os
from pathlib import Path
import sys
from unittest import SkipTest, TestCase

import dlsym


def importorskip(module):
    try:
        importlib.import_module(module)
    except ImportError:
        raise SkipTest("Could not import {!r}".format(module))


class TestDlsym(TestCase):

    def test_atan2(self):
        atan2 = CFUNCTYPE(c_double, c_double, c_double)(
            dlsym.dlsym("atan2"))
        assert atan2 and atan2(1, 2) == math.atan2(1, 2)

    def test_tcl(self):
        importorskip("tkinter")
        # Python calls Tcl_FindExecutable for us.
        getnameofexecutable = CFUNCTYPE(c_char_p)(
            dlsym.dlsym("Tcl_GetNameOfExecutable"))
        # On Windows, separators must be normalized.
        assert Path(os.fsdecode(getnameofexecutable())) == Path(sys.executable)

    def test_blas(self):
        importorskip("numpy")
        dasum = CFUNCTYPE(
            c_double, POINTER(c_int), POINTER(c_double), POINTER(c_int))(
                dlsym.dlsym("dasum_64_"))
        assert dasum and dasum(
            (c_int * 1)(10), (c_double * 10)(*range(10)), (c_int * 1)(1)) == 45

    def test_fftw(self):
        importorskip("pyfftw")
        alignment_of = CFUNCTYPE(c_int, POINTER(c_double))(
            dlsym.dlsym("fftw_alignment_of"))
        buf = (c_double * 10)(*range(10))
        a0 = alignment_of(buf)
        a1 = alignment_of(
            ctypes.cast(ctypes.addressof(buf) + ctypes.sizeof(c_double),
                        POINTER(c_double)))
        assert (a1 - a0) % ctypes.sizeof(c_double) == 0
