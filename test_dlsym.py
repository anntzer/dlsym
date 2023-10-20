import ctypes
from ctypes import CFUNCTYPE, POINTER, byref, c_double, c_int
import importlib
import math
from unittest import SkipTest, TestCase

import dlsym


def importorskip(module):
    try:
        return importlib.import_module(module)
    except ImportError:
        raise SkipTest("Could not import {!r}".format(module))


c_int_p = POINTER(ctypes.c_int)
c_double_p = POINTER(ctypes.c_double)


class TestDlsym(TestCase):

    def test_atan2(self):
        atan2 = CFUNCTYPE(c_double, c_double, c_double)(
            dlsym.dlsym("atan2"))
        self.assertTrue(atan2)
        self.assertEqual(atan2(1, 2), math.atan2(1, 2))

    def test_tcl(self):
        tkinter = importorskip("tkinter")
        # This test used to check Tcl_GetNameOfExecutable() == sys.executable,
        # but on macOS one can return a path in .../Resources/Python.app/...
        # and the other one a path outside of it.
        get_version = CFUNCTYPE(None, c_int_p, c_int_p, c_int_p, c_int_p)(
            dlsym.dlsym("Tcl_GetVersion"))
        a = c_int()
        b = c_int()
        get_version(byref(a), byref(b), byref(c_int()), byref(c_int()))
        self.assertEqual(f"{a.value}.{b.value}", str(tkinter.TclVersion))

    def test_blas(self):
        importorskip("numpy")
        dasum = CFUNCTYPE(c_double, c_int_p, c_double_p, c_int_p)(
            dlsym.dlsym("dasum_64_"))
        self.assertTrue(dasum)
        self.assertEqual(
            dasum(
                (c_int * 1)(10), (c_double * 10)(*range(10)), (c_int * 1)(1)),
            45)

    def test_fftw(self):
        importorskip("pyfftw")
        alignment_of = CFUNCTYPE(c_int, c_double_p)(
            dlsym.dlsym("fftw_alignment_of"))
        buf = (c_double * 10)(*range(10))
        a0 = alignment_of(buf)
        a1 = alignment_of(
            ctypes.cast(ctypes.addressof(buf) + ctypes.sizeof(c_double),
                        POINTER(c_double)))
        self.assertEqual((a1 - a0) % ctypes.sizeof(c_double), 0)
